# CyberLeigos — publicação no GitHub Pages

Este pacote já está pronto para o GitHub Pages: site 100% estático, `index.html` na raiz, caminhos relativos.

## Passo a passo
1. Extraia o ZIP e envie **todo o conteúdo** (não a pasta que o contém) para a raiz do repositório `DudsBite/CyberLeigos`, branch `main`. Substitua os arquivos antigos.
2. Em **Settings → Pages**, selecione *Deploy from a branch*, branch `main`, pasta `/ (root)`.
3. **Antes ou logo depois de publicar**, execute no Supabase (SQL Editor), nesta ordem:
   1. `sql/001_migracao_cyberleigos.sql`
   2. `sql/002_catalogo_atividades.sql`
   
   Sem isso o site abre normalmente, mas o XP de contas não é salvo e o ranking não carrega. Detalhes em `docs/MIGRACOES-SQL.md`.
4. Confira `docs/CONFIGURACAO-SUPABASE.md` (URLs de redirecionamento e confirmação de e-mail).
5. Para ativar o botão "Continuar com Google", siga `docs/GOOGLE-OAUTH.md`.
6. Acesse https://dudsbite.github.io/CyberLeigos/

`assets/supabase-config.js` contém a URL e a chave **publicável** do projeto Supabase já existente (preservada). Nunca coloque `service_role` ou outros segredos no repositório.

## Documentação técnica (não faz parte do site)
- `docs/PUBLICACAO-GITHUB-PAGES.md` · `docs/CONFIGURACAO-SUPABASE.md` · `docs/GOOGLE-OAUTH.md` · `docs/MIGRACOES-SQL.md` · `docs/ESTRUTURA-DO-PROJETO.md`
