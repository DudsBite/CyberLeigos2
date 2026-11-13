/* Simulação em memória do Supabase para testes automatizados no navegador (NÃO é publicada no site).
   Reproduz as regras das funções SQL: award_xp, get_ranking, get_my_rank, sync_profile. */
(function(){
  var K = 'mock_db_v1', S = 'mock_session_v1';
  function load(){ try{ return JSON.parse(localStorage.getItem(K)) || {users:{}, profiles:{}}; }catch(e){ return {users:{}, profiles:{}}; } }
  function save(db){ localStorage.setItem(K, JSON.stringify(db)); }
  var listeners = [];
  function session(){ try{ return JSON.parse(localStorage.getItem(S)); }catch(e){ return null; } }
  function emit(evt, s){ listeners.forEach(function(f){ f(evt, s); }); }
  var catalog = null;
  function today(){ return new Intl.DateTimeFormat('en-CA',{timeZone:'America/Sao_Paulo'}).format(new Date()); }
  function ok(data){ return Promise.resolve({data:data, error:null}); }
  function err(m, code){ return Promise.resolve({data:null, error:{message:m, code:code}}); }
  window.__mock = {reset:function(){ localStorage.removeItem(K); localStorage.removeItem(S); }, fail:false};
  window.supabase = {createClient: function(){
    var c = {
      auth:{
        getSession:function(){ return Promise.resolve({data:{session:session()}}); },
        onAuthStateChange:function(f){ listeners.push(f); return {data:{subscription:{}}}; },
        signInWithPassword:function(a){ var db = load(), u = db.users[a.email]; if(!u || u.password !== a.password) return err('Invalid login credentials', 'invalid_credentials');
          var s = {user:u.user, access_token:'x'}; localStorage.setItem(S, JSON.stringify(s)); setTimeout(function(){ emit('SIGNED_IN', s); }, 0); return ok({user:u.user, session:s}); },
        signUp:function(a){ var db = load(); if(db.users[a.email]) return ok({user:{identities:[]}, session:null});
          var id = 'u-' + Math.random().toString(16).slice(2, 10), user = {id:id, email:a.email, created_at:new Date().toISOString(), user_metadata:(a.options||{}).data || {}, identities:[{}]};
          db.users[a.email] = {password:a.password, user:user, confirmed:false}; save(db); return ok({user:user, session:null}); },
        signInWithOAuth:function(a){ window.__oauth = a; return ok({}); },
        signOut:function(){ localStorage.removeItem(S); setTimeout(function(){ emit('SIGNED_OUT', null); }, 0); return Promise.resolve({error:null}); },
        resetPasswordForEmail:function(e, o){ window.__reset = {email:e, o:o}; return ok({}); },
        updateUser:function(p){ var s = session(); if(!s) return err('not logged'); var db = load(); db.users[s.user.email].password = p.password; save(db); return ok({}); }
      },
      from:function(t){ var st = {sel:null, patch:null, id:null};
        var q = {select:function(){ st.sel = true; return q; }, eq:function(k, v){ st.id = v; return q; }, update:function(p){ st.patch = p; return q; },
          maybeSingle:function(){ var db = load(), p = db.profiles[st.id]; if(st.patch){ if(!p) return ok(null); Object.keys(st.patch).forEach(function(k){ p[k] = st.patch[k]; }); save(db); }
            return ok(p ? JSON.parse(JSON.stringify(p)) : null); }};
        return q; },
      rpc:function(name, a){
        if(window.__mock.fail) return Promise.reject(new TypeError('Failed to fetch'));
        var s = session(), db = load();
        if(name === 'get_ranking'){ var rows = Object.keys(db.profiles).map(function(id){ return Object.assign({id:id}, db.profiles[id]); }).filter(function(p){ return p.xp > 0; }).sort(function(x, y){ return y.xp - x.xp; });
          var out = rows.map(function(p, i){ var rk = rows.filter(function(o){ return o.xp > p.xp; }).length + 1; return {rank:rk, user_id:p.id, display_name:p.display_name || 'Aprendiz', avatar_url:p.avatar_url || null, xp:p.xp, total_count:rows.length}; });
          return ok(out.slice(a.p_offset, a.p_offset + a.p_limit)); }
        if(!s) return err('not_authenticated', '28000');
        var id = s.user.id, p = db.profiles[id] = db.profiles[id] || {xp:0, completed:[], daily:{}, streak:0, last_day:null};
        if(name === 'sync_profile'){ if(!p.display_name && a.p_display_name) p.display_name = a.p_display_name; if(!p.avatar_url && a.p_avatar_url) p.avatar_url = a.p_avatar_url; save(db); return ok(null); }
        if(name === 'get_my_rank'){ var better = Object.keys(db.profiles).filter(function(k){ return db.profiles[k].xp > p.xp; }).length; return ok([{rank:p.xp > 0 ? better + 1 : null, xp:p.xp, total:Object.keys(db.profiles).filter(function(k){ return db.profiles[k].xp > 0; }).length}]); }
        if(name === 'award_xp'){
          var aid = a.p_activity_id, xp = 0, m;
          if((m = /^daily-(\d{4}-\d\d-\d\d)-([0-2]|bonus)$/.exec(aid))){ if(m[1] !== today()) return ok({awarded:false, reason:'wrong_day', xp:p.xp});
            if(m[2] === 'bonus'){ if([0,1,2].some(function(i){ return p.completed.indexOf('daily-' + m[1] + '-' + i) < 0; })) return ok({awarded:false, reason:'incomplete', xp:p.xp}); xp = 15; } else xp = 10; }
          else { var C = window.CL.catalogGet(aid); if(!C) return ok({awarded:false, reason:'unknown', xp:p.xp}); xp = C.xp; }
          if(p.completed.indexOf(aid) > -1) return ok({awarded:false, reason:'already', xp:p.xp, streak:p.streak, last_day:p.last_day, completed:p.completed, daily:p.daily});
          p.xp += xp; p.completed.push(aid); if(/^daily-/.test(aid)) p.daily[aid] = true; p.streak = Math.max(1, p.streak); p.last_day = today(); save(db);
          return ok({awarded:true, reason:'ok', xp_gained:xp, xp:p.xp, streak:p.streak, last_day:p.last_day, completed:p.completed, daily:p.daily});
        }
        return err('unknown rpc');
      }
    };
    return c;
  }};
  // permite que o teste confirme e-mail e simule OAuth
  window.__mock.confirm = function(email){ var db = load(); db.users[email].confirmed = true; save(db); };
  window.__mock.loginAs = function(user){ var s = {user:user, access_token:'x'}; localStorage.setItem(S, JSON.stringify(s)); emit('SIGNED_IN', s); };
})();
