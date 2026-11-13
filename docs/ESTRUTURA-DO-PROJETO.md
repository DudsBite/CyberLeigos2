# Estrutura do projeto

```
index.html …                páginas (geradas por tools/build_pages.py)
assets/supabase-config.js   URL + chave publicável do Supabase (preservado)
assets/css/style.css        estilos compartilhados · games.css (minigames)
assets/js/core.js           utilitários, fuso, níveis, avatares, catálogo de XP
assets/js/auth.js           Supabase Auth, cabeçalho, menu de usuário
assets/js/progress.js       XP, sincronização, tarefas diárias (seleção por data)
assets/js/app.js · fx.js    inicialização · fundo interativo, menus, transições
assets/js/data/*.js         conteúdo: lições, quizzes, tarefas, glossário, minigames
assets/js/pages/*.js        um script por página
assets/js/games/*.js        7 minigames + shell.js (introdução, resultado, XP)
sql/                        migrações
docs/                       documentação técnica
tools/                      build_pages.py (cabeçalho/rodapé), gerar_catalogo.js
tests/                      testes de navegador com Supabase simulado
```
- Para mudar cabeçalho, rodapé ou páginas: edite `tools/build_pages.py` e rode `python3 tools/build_pages.py`.
- Para alterar conteúdo: edite `assets/js/data/*.js` (e rode `node tools/gerar_catalogo.js` + execute o novo `002`).
- Endereços antigos (`golpes.html`, `malwares.html` …) caem na página 404, que redireciona para a lição equivalente.
- `tests/smoke.py` (Python + Playwright) roda 118 verificações com `tests/mock-supabase.js`.
