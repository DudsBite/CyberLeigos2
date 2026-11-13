-- =====================================================================
-- CyberLeigos — migração 001 (segura para executar mais de uma vez)
-- Preserva a tabela public.profiles e todos os dados existentes.
-- Execute no Supabase: SQL Editor > New query > cole e rode (Run).
-- Depois rode também 002_catalogo_atividades.sql.
-- =====================================================================

-- 1) Novas colunas públicas de perfil (sem apagar nada) -----------------
alter table public.profiles add column if not exists display_name text;
alter table public.profiles add column if not exists avatar_url   text;
alter table public.profiles add column if not exists created_at   timestamptz not null default now();

do $$ begin
  if not exists (select 1 from pg_constraint where conname = 'profiles_display_name_len') then
    alter table public.profiles add constraint profiles_display_name_len
      check (display_name is null or char_length(display_name) between 2 and 30) not valid;
  end if;
  if not exists (select 1 from pg_constraint where conname = 'profiles_avatar_url_fmt') then
    alter table public.profiles add constraint profiles_avatar_url_fmt
      check (avatar_url is null or (char_length(avatar_url) <= 500 and avatar_url ~ '^(preset:[a-z0-9-]+|https://[^[:space:]<>"'']+)$')) not valid;
  end if;
end $$;

-- 2) RLS: cada pessoa só enxerga e altera a própria linha ---------------
alter table public.profiles enable row level security;
drop policy if exists "Users read own profile"   on public.profiles;
drop policy if exists "Users insert own profile" on public.profiles;
drop policy if exists "Users update own profile" on public.profiles;
create policy "Users read own profile"   on public.profiles for select using (auth.uid() = id);
create policy "Users insert own profile" on public.profiles for insert with check (auth.uid() = id);
create policy "Users update own profile" on public.profiles for update using (auth.uid() = id) with check (auth.uid() = id);

-- 3) Privilégios por coluna: o navegador NÃO pode alterar XP, progresso,
--    sequência ou datas. Só nome e avatar podem ser editados diretamente.
revoke all on public.profiles from anon, authenticated;
grant select on public.profiles to authenticated;
grant insert (id, display_name, avatar_url) on public.profiles to authenticated;
grant update (display_name, avatar_url)     on public.profiles to authenticated;

-- 4) Catálogo de atividades que podem render XP (valores definidos no servidor)
create table if not exists public.activity_catalog (
  id   text primary key,
  kind text not null,
  xp   integer not null check (xp > 0)
);
alter table public.activity_catalog enable row level security;   -- sem políticas = inacessível ao navegador
revoke all on public.activity_catalog from anon, authenticated;

-- 5) Sincroniza nome/foto iniciais (só preenche se estiverem vazios) ----
create or replace function public.sync_profile(p_display_name text default null, p_avatar_url text default null)
returns void
language plpgsql
security definer
set search_path = public, pg_temp
as $$
declare
  v_uid  uuid := auth.uid();
  v_name text;
  v_avatar text;
begin
  if v_uid is null then raise exception 'not_authenticated' using errcode = '28000'; end if;
  v_name := left(btrim(regexp_replace(coalesce(p_display_name, ''), '[[:cntrl:]<>]', '', 'g')), 30);
  if char_length(v_name) < 2 then v_name := null; end if;
  v_avatar := case when char_length(p_avatar_url) <= 500 and p_avatar_url ~ '^https://[^[:space:]<>"'']+$' then p_avatar_url else null end;
  insert into public.profiles (id, display_name, avatar_url) values (v_uid, v_name, v_avatar)
  on conflict (id) do update set
    display_name = coalesce(nullif(public.profiles.display_name, ''), excluded.display_name),
    avatar_url   = coalesce(nullif(public.profiles.avatar_url, ''),   excluded.avatar_url);
end $$;

-- 6) Concede XP: única forma de aumentar pontos ------------------------
create or replace function public.award_xp(p_activity_id text)
returns jsonb
language plpgsql
security definer
set search_path = public, pg_temp
as $$
declare
  v_uid   uuid := auth.uid();
  v_today date := (now() at time zone 'America/Sao_Paulo')::date;
  v_xp    integer;
  v_day   date;
  v_streak integer;
  p       public.profiles%rowtype;
begin
  if v_uid is null then raise exception 'not_authenticated' using errcode = '28000'; end if;
  if p_activity_id is null or char_length(p_activity_id) > 80 then
    return jsonb_build_object('awarded', false, 'reason', 'invalid');
  end if;

  insert into public.profiles (id) values (v_uid) on conflict (id) do nothing;
  select * into p from public.profiles where id = v_uid for update;

  if p_activity_id ~ '^daily-[0-9]{4}-[0-9]{2}-[0-9]{2}-([0-2]|bonus)$' then
    begin v_day := substring(p_activity_id from 7 for 10)::date;
    exception when others then return jsonb_build_object('awarded', false, 'reason', 'invalid'); end;
    if v_day <> v_today then
      return jsonb_build_object('awarded', false, 'reason', 'wrong_day', 'xp', p.xp);
    end if;
    if p_activity_id like '%-bonus' then
      if not (p.completed @> to_jsonb('daily-' || v_day::text || '-0') and
              p.completed @> to_jsonb('daily-' || v_day::text || '-1') and
              p.completed @> to_jsonb('daily-' || v_day::text || '-2')) then
        return jsonb_build_object('awarded', false, 'reason', 'incomplete', 'xp', p.xp);
      end if;
      v_xp := 15;
    else
      v_xp := 10;
    end if;
  else
    select c.xp into v_xp from public.activity_catalog c where c.id = p_activity_id;
    if v_xp is null then return jsonb_build_object('awarded', false, 'reason', 'unknown', 'xp', p.xp); end if;
  end if;

  if p.completed @> to_jsonb(p_activity_id) then
    return jsonb_build_object('awarded', false, 'reason', 'already', 'xp', p.xp, 'streak', p.streak,
      'last_day', p.last_day, 'completed', p.completed, 'daily', p.daily);
  end if;

  v_streak := case
    when p.last_day = v_today then greatest(p.streak, 1)
    when p.last_day = v_today - 1 then p.streak + 1
    else 1 end;

  update public.profiles set
    xp        = xp + v_xp,
    completed = completed || to_jsonb(p_activity_id),
    daily     = case when p_activity_id like 'daily-%' then daily || jsonb_build_object(p_activity_id, true) else daily end,
    streak    = v_streak,
    last_day  = v_today,
    updated_at = now()
  where id = v_uid
  returning * into p;

  return jsonb_build_object('awarded', true, 'reason', 'ok', 'xp_gained', v_xp, 'xp', p.xp, 'streak', p.streak,
    'last_day', p.last_day, 'completed', p.completed, 'daily', p.daily);
end $$;

-- 7) Ranking público: apenas nome, avatar, XP e identificador ----------
create or replace function public.get_ranking(p_limit integer default 20, p_offset integer default 0)
returns table (rank bigint, user_id uuid, display_name text, avatar_url text, xp integer, total_count bigint)
language sql
stable
security definer
set search_path = public, pg_temp
as $$
  with r as (
    select p.id, coalesce(nullif(p.display_name, ''), 'Aprendiz') as dn, p.avatar_url as av, p.xp as pts,
           rank() over (order by p.xp desc) as rk,
           row_number() over (order by p.xp desc, p.updated_at asc, p.id) as rn,
           count(*) over () as tc
    from public.profiles p
    where p.xp > 0
  )
  select r.rk, r.id, r.dn, r.av, r.pts, r.tc
  from r order by r.rn
  limit least(greatest(coalesce(p_limit, 20), 1), 100)
  offset greatest(coalesce(p_offset, 0), 0);
$$;

create or replace function public.get_my_rank()
returns table (rank bigint, xp integer, total bigint)
language sql
stable
security definer
set search_path = public, pg_temp
as $$
  select case when me.xp > 0 then (select count(*) + 1 from public.profiles o where o.xp > me.xp) end,
         me.xp,
         (select count(*) from public.profiles o where o.xp > 0)
  from public.profiles me where me.id = auth.uid();
$$;

-- 8) Permissões de execução ---------------------------------------------
revoke all on function public.sync_profile(text, text) from public, anon;
revoke all on function public.award_xp(text)           from public, anon;
revoke all on function public.get_ranking(integer, integer) from public;
revoke all on function public.get_my_rank()            from public, anon;
grant execute on function public.sync_profile(text, text)      to authenticated;
grant execute on function public.award_xp(text)                to authenticated;
grant execute on function public.get_my_rank()                 to authenticated;
grant execute on function public.get_ranking(integer, integer) to anon, authenticated;
