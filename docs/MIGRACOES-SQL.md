# Migrações SQL

Execute no **SQL Editor** do Supabase, nesta ordem. Ambos podem ser executados mais de uma vez.

| Arquivo | O que faz |
|---|---|
| `sql/001_migracao_cyberleigos.sql` | Acrescenta `display_name`, `avatar_url`, `created_at` em `public.profiles` (dados existentes preservados); refaz as políticas RLS (cada usuário só vê a própria linha); **revoga** a gravação direta de `xp`, `completed`, `daily`, `streak`, `last_day`; cria `activity_catalog`, `sync_profile`, `award_xp`, `get_ranking`, `get_my_rank`. |
| `sql/002_catalogo_atividades.sql` | Preenche o catálogo (73 atividades: lições, perguntas de quiz, bônus e minigames) com o XP de cada uma. Gerado por `node tools/gerar_catalogo.js` — rode de novo se mudar lições, quizzes ou minigames. |

## Regras aplicadas pelo banco
- `award_xp(id)`: exige login; só aceita ids do catálogo ou `daily-AAAA-MM-DD-0..2/bonus`; tarefas diárias só valem no dia atual (fuso `America/Sao_Paulo`); o bônus exige as 3 tarefas do dia; cada id rende XP uma única vez (trava de linha contra chamadas simultâneas); calcula a sequência de dias.
- `get_ranking(limit, offset)`: apenas usuários com XP > 0; retorna posição (empates dividem a posição), id, nome, avatar, XP e total. Executável por visitantes e usuários.
- `get_my_rank()`: posição do usuário logado.
- Restrição `avatar_url`: só `preset:<id>` ou `https://…` (bloqueia `javascript:`); `display_name`: 2–30 caracteres.

## Atenção
Depois da migração, versões antigas do site que gravavam `xp` direto na tabela deixam de funcionar. Publique o site novo junto.

Os scripts foram testados em PostgreSQL 16 local com um esquema `auth` simulado (permissões, dedupe, ranking, empates, anon sem acesso a `award_xp`). Não foram executados no seu projeto Supabase real.
