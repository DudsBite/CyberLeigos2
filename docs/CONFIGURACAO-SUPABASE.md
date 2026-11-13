# Configuração do Supabase

O projeto Supabase existente (URL e chave publicável em `assets/supabase-config.js`) é preservado. Cadastro, confirmação de e-mail, login, logout e a tabela `public.profiles` continuam os mesmos; a migração apenas **acrescenta** colunas e funções.

## 1. Authentication → URL Configuration
- **Site URL:** `https://dudsbite.github.io/CyberLeigos/`
- **Redirect URLs:** `https://dudsbite.github.io/CyberLeigos/**`
  (cobre `index`, `redefinir-senha.html` e o retorno do Google). Para testes locais adicione também `http://localhost:8000/**`.

## 2. Authentication → Providers → Email
- Mantenha **Confirm email** ativado (o site mostra "confirme seu e-mail" e só considera o usuário logado quando existe sessão válida).
- Opcional: SMTP próprio, pois o serviço padrão tem limite de envios.
- Opcional: personalize os modelos de e-mail (*Confirm signup* e *Reset password*) em português.

## 3. Banco de dados
Execute os scripts de `sql/` (ver `MIGRACOES-SQL.md`).

## 4. Fluxo de recuperação de senha
`recuperar-senha.html` → e-mail do Supabase → `redefinir-senha.html` (define a nova senha). Links expirados/usados mostram mensagem amigável e oferecem pedir outro.

## 5. Segurança
- Somente a chave **publicável** está no site. Nunca publique `service_role`.
- XP, progresso, sequência e datas **não podem ser gravados pelo navegador**: só a função `award_xp` (SECURITY DEFINER) altera esses campos, e apenas para atividades do catálogo, uma vez por atividade.
- O ranking usa a função `get_ranking`, que devolve só nome de exibição, avatar, XP e id do usuário. E-mails nunca são expostos.
- Limite conhecido: as respostas dos quizzes são conferidas no navegador. Um usuário técnico pode concluir atividades sem responder, mas só ganha o XP finito do catálogo, uma vez cada, sem como editar XP livremente.
