# Login com Google (Supabase Auth)

O botão "Continuar com Google" chama `signInWithOAuth({provider:'google'})` com retorno para `https://dudsbite.github.io/CyberLeigos/`. **Só funciona depois de configurar o provedor**; sem isso o site mostra "Não foi possível entrar com o Google. Tente novamente ou utilize seu e-mail e senha."

## Passos (feitos por você, nenhum segredo vai para o repositório)
1. Google Cloud Console → *APIs e serviços* → *Tela de permissão OAuth*: configure o app (nome CyberLeigos, e-mail de suporte, escopos `email`, `profile`, `openid`).
2. *Credenciais* → *Criar credenciais* → *ID do cliente OAuth* → tipo **Aplicativo da Web**.
   - **Origens JavaScript autorizadas:** `https://dudsbite.github.io`
   - **URIs de redirecionamento autorizados:** `https://ieebinjdnxgqntjzadrv.supabase.co/auth/v1/callback`
3. Copie o **Client ID** e o **Client Secret**.
4. Supabase → *Authentication → Providers → Google*: ative, cole Client ID e Secret e salve. (O Secret fica só no Supabase.)
5. Supabase → *Authentication → URL Configuration*: confirme que `https://dudsbite.github.io/CyberLeigos/**` está em *Redirect URLs*.

## Como o site usa os dados
Após o retorno, a sessão é criada, `sync_profile` preenche nome e foto (metadados `full_name`/`name` e `avatar_url`/`picture` do Google) **somente se o perfil ainda estiver vazio**, e o cabeçalho mostra nome e foto. O usuário pode trocar nome e avatar em `perfil.html`.

## Teste
Entre com uma conta Google, confira cabeçalho, perfil e ranking; saia e entre de novo.
