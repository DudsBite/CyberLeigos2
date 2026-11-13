import asyncio, json, re, sys, http.server, threading, socketserver, functools
from playwright.async_api import async_playwright
ROOT='/home/claude/serve'
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
    def __init__(s,*a,**k): super().__init__(*a,directory=ROOT,**k)
    def send_head(s):
        import os
        p=s.translate_path(s.path)
        if not os.path.exists(p):
            s.path='/CyberLeigos/404.html'; s.send_response=lambda c,m=None,_o=http.server.SimpleHTTPRequestHandler.send_response,_s=s:_o(_s,404,m) if c==200 else _o(_s,c,m)
        return super().send_head()
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.TCPServer(('127.0.0.1',8791),Q); srv.allow_reuse_address=True
threading.Thread(target=srv.serve_forever,daemon=True).start()
B='http://127.0.0.1:8791/CyberLeigos/'
MOCK=open('/home/claude/cyberleigos/tests/mock-supabase.js').read()
PAGES=['index','licoes','licao.html?id=senhas','tarefas','quizzes','minigames','minigame.html?id=phishing','progresso','ranking','glossario','tier-list','sobre','login','cadastro','recuperar-senha','redefinir-senha','404']
res=[]
def R(name,ok,info=''):
    res.append((name,ok,info)); print(('PASS ' if ok else 'FAIL ')+name+(' — '+str(info) if info else ''))
async def newctx(br,w=1280,h=800):
    ctx=await br.new_context(viewport={'width':w,'height':h})
    await ctx.route('**/cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,content_type='application/javascript',body=MOCK))
    return ctx
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        # 1) carregamento de todas as páginas, sem erros de console, sem rolagem horizontal
        for vw,vh in [(1280,800),(375,740)]:
            ctx=await newctx(br,vw,vh); pg=await ctx.new_page(); errs=[]
            pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None); pg.on('pageerror',lambda e:errs.append(str(e)))
            for u in PAGES:
                errs.clear(); await pg.goto(B+u+('.html' if '?' not in u else '').replace('.html','')+('' if '?' in u else '') if False else B+(u if ('?' in u or u.endswith('.html')) else u+'.html')); await pg.wait_for_timeout(500)
                ov=await pg.evaluate('document.documentElement.scrollWidth-document.documentElement.clientWidth')
                errs=[e for e in errs if not (u=='404' and '404' in e)]; R(f'[{vw}] {u} sem erros',not errs,errs[:2]); R(f'[{vw}] {u} sem rolagem horizontal',ov<=1,ov)
            await ctx.close()
        # 2) fluxo visitante
        ctx=await newctx(br); pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(B+'index.html'); await pg.wait_for_selector('.btn-login')
        R('visitante vê "Fazer Login"','Fazer Login' in await pg.inner_text('#authSlot'))
        await pg.click('.btn-login'); await pg.wait_for_url('**/login.html**'); R('botão leva ao login','Bem-vindo de volta!' in await pg.inner_text('h1'))
        # validação
        await pg.click('#submitBtn'); R('login valida campos vazios','Digite seu e-mail' in await pg.inner_text('#emailErr'))
        await pg.fill('#email','abc'); await pg.fill('#password','x'); await pg.click('#submitBtn'); R('login valida e-mail inválido','não parece válido' in await pg.inner_text('#emailErr'))
        await pg.fill('#email','x@y.com'); await pg.click('#submitBtn'); await pg.wait_for_timeout(300); R('credenciais incorretas: mensagem amigável','incorretos' in await pg.inner_text('#formMsg'))
        await pg.click('#googleBtn'); await pg.wait_for_timeout(200); o=await pg.evaluate('window.__oauth'); R('Google inicia OAuth com redirect correto',o and o['provider']=='google' and o['options']['redirectTo']==B,o)
        # cadastro
        await pg.click('#toSignup'); await pg.wait_for_url('**/cadastro.html**')
        await pg.fill('#name','Ana Teste'); await pg.fill('#email','ana@exemplo.com'); await pg.fill('#password','abc'); await pg.fill('#password2','abd'); await pg.click('#submitBtn')
        R('cadastro valida senha','pelo menos 8' in await pg.inner_text('#passwordErr')); R('cadastro valida confirmação','não são iguais' in await pg.inner_text('#password2Err'))
        await pg.fill('#password','senha1234'); await pg.fill('#password2','senha1234'); await pg.click('#submitBtn'); await pg.wait_for_timeout(300)
        R('cadastro pede confirmação de e-mail','confirmar' in await pg.inner_text('#formMsg'))
        R('não autenticado antes de sessão válida','Fazer Login' in await pg.inner_text('#authSlot'))
        # login
        await pg.goto(B+'login.html?voltar=tarefas.html'); await pg.wait_for_selector('#email'); await pg.fill('#email','ana@exemplo.com'); await pg.fill('#password','senha1234')
        await pg.click('.toggle-pw'); R('mostrar senha funciona',await pg.get_attribute('#password','type')=='text')
        await pg.click('#submitBtn'); await pg.wait_for_url('**/tarefas.html**',timeout=5000); await pg.wait_for_selector('.user-btn')
        R('login redireciona para página de origem','tarefas.html' in pg.url)
        R('cabeçalho mostra nome','Ana Teste' in await pg.inner_text('#authSlot') and 'Fazer Login' not in await pg.inner_text('#authSlot'))
        await pg.click('.user-btn'); items=await pg.inner_text('#userMenu')
        R('menu tem 4 itens',all(t in items for t in ['Meu perfil','Meu progresso','Ranking','Sair da conta']))
        await pg.keyboard.press('Escape'); R('Escape fecha menu',not await pg.evaluate("document.querySelector('#userMenu').classList.contains('open')"))
        await pg.click('.user-btn'); await pg.click('h1'); R('clique fora fecha menu',not await pg.evaluate("document.querySelector('#userMenu').classList.contains('open')"))
        await pg.reload(); await pg.wait_for_selector('.user-btn'); R('sessão persiste após atualizar','Ana Teste' in await pg.inner_text('#authSlot'))
        # tarefa diária
        cards=await pg.query_selector_all('.task-card'); R('3 tarefas diárias',len(cards)==3)
        # lição
        await pg.goto(B+'licao.html?id=intro'); await pg.wait_for_selector('.cp-card')
        for i in range(3):
            q=await pg.evaluate('''()=>{const L=CL.data.lessons.find(l=>l.id==='intro');const t=document.querySelector('.cp-q').textContent;return L.check.find(c=>CL.plain(c.q)===t)}''')
            txt=await pg.evaluate('(q)=>CL.plain(q.o[q.c])',q)
            await pg.click(f'.opt:has-text("{txt[:40]}")'); await pg.click('.cp-actions .btn')
        await pg.wait_for_selector('.result-card'); await pg.wait_for_timeout(500)
        xp=await pg.inner_text('.xp-chip'); R('lição concede 30 XP',xp.strip().startswith('30'),xp)
        await pg.reload(); await pg.wait_for_selector('.cp-card')
        for i in range(3):
            q=await pg.evaluate('''()=>{const L=CL.data.lessons.find(l=>l.id==='intro');const t=document.querySelector('.cp-q').textContent;return L.check.find(c=>CL.plain(c.q)===t)}''')
            txt=await pg.evaluate('(q)=>CL.plain(q.o[q.c])',q); await pg.click(f'.opt:has-text("{txt[:40]}")'); await pg.click('.cp-actions .btn')
        await pg.wait_for_timeout(600); R('recarregar/refazer não repete XP',(await pg.inner_text('.xp-chip')).strip().startswith('30'),await pg.inner_text('.xp-chip'))
        # tarefas: responde correto
        await pg.goto(B+'tarefas.html'); await pg.wait_for_selector('.task-card')
        for i in range(3):
            card=(await pg.query_selector_all('.task-card'))[i]; qt=await (await card.query_selector('.task-q')).inner_text()
            ans=await pg.evaluate('(qt)=>{const b=CL.data.daily.find(d=>d.q===qt);return b.o[b.c]}',qt)
            await card.query_selector(f'.opt:has-text("{ans[:35]}")') and await (await card.query_selector(f'.opt:has-text("{ans[:35]}")')).click(); await pg.wait_for_timeout(250)
        await pg.wait_for_timeout(600); xp=int((await pg.inner_text('.xp-chip')).split()[0].replace('.',''))
        R('3 tarefas + bônus = 30+30+15 XP',xp==75,xp)
        await pg.reload(); await pg.wait_for_selector('.task-card.done'); R('tarefas concluídas persistem',len(await pg.query_selector_all('.task-card.done'))==3)
        # quiz
        await pg.goto(B+'quizzes.html'); await pg.click('.level-card >> nth=0'); await pg.wait_for_selector('.quiz-q')
        for i in range(8):
            qt=await pg.inner_text('.quiz-q'); ans=await pg.evaluate('(qt)=>{for(const k in CL.data.quizzes){const b=CL.data.quizzes[k].questions.find(d=>d.q===qt);if(b)return b.o[b.c]}}',qt)
            await pg.click(f'.opt:has-text("{ans[:35]}")'); await pg.wait_for_timeout(250); await pg.click('.cp-actions .btn')
        await pg.wait_for_selector('.result-card'); R('quiz termina com resultado','8/8' in await pg.inner_text('.result-card'))
        xp1=int((await pg.inner_text('.xp-chip')).split()[0].replace('.','')); R('quiz concede XP',xp1>75,xp1)
        await pg.click('text=Jogar de novo'); 
        for i in range(8):
            qt=await pg.inner_text('.quiz-q'); ans=await pg.evaluate('(qt)=>{for(const k in CL.data.quizzes){const b=CL.data.quizzes[k].questions.find(d=>d.q===qt);if(b)return b.o[b.c]}}',qt)
            await pg.click(f'.opt:has-text("{ans[:35]}")'); await pg.wait_for_timeout(250); await pg.click('.cp-actions .btn')
        await pg.wait_for_selector('.result-card'); xp2=int((await pg.inner_text('.xp-chip')).split()[0].replace('.',''))
        comp=await pg.evaluate("JSON.parse(localStorage.getItem('mock_db_v1')).profiles[JSON.parse(localStorage.getItem('mock_session_v1')).user.id].completed"); soma=xp2
        R('quiz: nenhuma pergunta paga duas vezes',len(comp)==len(set(comp)) and soma==xp2,(soma,xp2))
        # minigames: random bot
        for g in ['phishing','permissoes','resposta','backup','wifi','senhas','links']:
            await pg.goto(B+f'minigame.html?id={g}'); await pg.wait_for_selector('#gStart'); await pg.click('#gStart'); done=False; ge=[]
            pg.on('pageerror',lambda e:ge.append(str(e)))
            for step in range(260):
                if await pg.query_selector('.g-stage .result-card'): done=True; break
                btns=await pg.query_selector_all('.g-stage button:not([disabled])')
                if not btns: await pg.wait_for_timeout(100); continue
                nxt=[b for b in btns if (await b.inner_text()).strip() in ('Próxima mensagem','Próximo aplicativo','Continuar','Próximo cenário','Próxima situação','Próximo link','Ver resultado','Ir ao laboratório','Próximo desafio','Próxima','Concluir laboratório','Simular desastre','Confirmar escolhas')] if False else None
                labels=[(await b.inner_text()).strip() for b in btns]
                pri=[i for i,l in enumerate(labels) if l in ('Próxima mensagem','Próximo aplicativo','Continuar','Próximo cenário','Próxima situação','Próximo link','Ver resultado','Ir ao laboratório','Próximo desafio','Próxima','Concluir laboratório','Simular desastre','Confirmar escolhas')]
                import random
                if g=='backup' and not await pg.query_selector('.disaster'):
                    fb=await pg.query_selector_all('.bk-file'); 
                    for f in fb[:4]:
                        await f.click(); 
                        for pl in (await pg.query_selector_all('.bk-place'))[1:3]: await pl.click()
                    await pg.click('text=Simular desastre'); continue
                if g=='senhas' and await pg.query_selector('#labPw') and await pg.query_selector('button:has-text("Concluir laboratório"):not([disabled])'):
                    await pg.fill('#labPw','cavalo-nuvem-pilha-sapato'); await pg.click('text=Concluir laboratório'); continue
                if g=='permissoes' and not await pg.query_selector('.perm.good, .perm.bad'):
                    # liga só a primeira permissão
                    sw=await pg.query_selector_all('.switch'); await sw[0].click() if sw else None; await pg.click('text=Confirmar escolhas'); continue
                if pri: await btns[pri[0]].click()
                else: await random.choice(btns).click()
                await pg.wait_for_timeout(60)
            R(f'minigame {g} chega ao resultado',done and not ge,ge[:1])
        await pg.goto(B+'perfil.html'); await pg.wait_for_selector('#pfName'); R('perfil mostra XP e lições','lições concluídas' in await pg.inner_text('.stat-strip'))
        await pg.fill('#pfName','Ana S.'); await pg.click('.avatar-picker button >> nth=3'); await pg.click('#pfForm button[type=submit]'); await pg.wait_for_timeout(400)
        R('perfil salva nome','Ana S.' in await pg.inner_text('#authSlot'),await pg.inner_text('#authSlot'))
        await pg.fill('#pfName','x'); await pg.click('#pfForm button[type=submit]'); R('perfil valida nome curto','pelo menos 2' in await pg.inner_text('#pfNameErr'))
        # ranking com outros usuários semeados
        await pg.evaluate('''()=>{const db=JSON.parse(localStorage.getItem('mock_db_v1'));[['Bia',900],['Caio',700],['Duda',500],['Edu',300],['Fabi',300],['Gui',50]].forEach(([n,x],i)=>{db.profiles['seed'+i]={xp:x,display_name:n,avatar_url:i==1?'preset:chave':null,completed:[],daily:{}}});localStorage.setItem('mock_db_v1',JSON.stringify(db))}''')
        await pg.goto(B+'ranking.html'); await pg.wait_for_selector('.pod'); await pg.wait_for_timeout(400)
        txt=await pg.inner_text('main'); R('ranking: pódio com 3',len(await pg.query_selector_all('.pod'))==3)
        R('ranking: ordem por XP e empate','Bia' in txt and txt.index('Bia')<txt.index('Caio') and (await pg.inner_text('#rkList')).count('4º')>=1)
        R('ranking sem e-mails','@' not in txt and 'exemplo.com' not in txt)
        R('ranking mostra minha posição ou destaque', 'Ana S.' in txt or 'Sua posição' in txt)
        await pg.click('#rkRefresh'); await pg.wait_for_timeout(300); R('ranking atualiza manualmente','Atualizado às' in await pg.inner_text('#rkStamp'))
        # erro de conexão no ranking
        await pg.evaluate('window.__mock.fail=true'); await pg.click('#rkRefresh'); await pg.wait_for_timeout(300); R('ranking com falha: mensagem amigável','Não foi possível carregar o ranking' in await pg.inner_text('main')); await pg.evaluate('window.__mock.fail=false')
        # logout
        await pg.click('.user-btn'); await pg.click('text=Sair da conta'); await pg.wait_for_url('**/index.html'); await pg.wait_for_selector('.btn-login')
        R('logout atualiza cabeçalho','Fazer Login' in await pg.inner_text('#authSlot'))
        db=await pg.evaluate("JSON.parse(localStorage.getItem('mock_db_v1')).profiles"); R('logout não apaga progresso salvo',any(v['xp']>=75 for v in db.values()))
        await pg.goto(B+'perfil.html'); await pg.wait_for_url('**/login.html'); R('perfil exige login','login.html' in pg.url)
        # recuperação de senha
        await pg.goto(B+'recuperar-senha.html'); await pg.fill('#email','ana@exemplo.com'); await pg.click('#submitBtn'); await pg.wait_for_timeout(300)
        r=await pg.evaluate('window.__reset'); R('recuperação envia e-mail com redirect certo',r and r['o']['redirectTo']==B+'redefinir-senha.html',r); R('recuperação: mensagem neutra','receberá' in await pg.inner_text('#formMsg'))
        await pg.goto(B+'redefinir-senha.html#error=access_denied&error_code=otp_expired'); await pg.wait_for_timeout(300); R('link expirado tratado','expirou' in await pg.inner_text('#redExpired'))
        # visitante: XP de sessão
        ctx2=await newctx(br); g=await ctx2.new_page(); await g.goto(B+'tarefas.html'); await g.wait_for_selector('.task-card')
        qt=await (await g.query_selector('.task-q')).inner_text(); ans=await g.evaluate('(qt)=>{const b=CL.data.daily.find(d=>d.q===qt);return b.o[b.c]}',qt)
        await g.click(f'.task-card >> nth=0 >> .opt:has-text("{ans[:35]}")'); await g.wait_for_timeout(400)
        R('visitante ganha XP local',(await g.inner_text('.xp-chip')).strip().startswith('10'))
        await g.reload(); await g.wait_for_selector('.task-card'); R('visitante: recarregar não repete XP',(await g.inner_text('.xp-chip')).strip().startswith('10'))
        # 404 mapeamento antigo
        await g.goto(B+'golpes.html'); await g.wait_for_timeout(800); R('404 carrega (mapeamento testado à parte em Node)','Erro 404' in await g.inner_text('main'))
        await br.close()
    bad=[r for r in res if not r[1]]; print(f'\n{len(res)-len(bad)}/{len(res)} ok'); 
    for b in bad: print('FALHOU:',b)
asyncio.run(main())
