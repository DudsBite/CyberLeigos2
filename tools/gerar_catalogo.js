// Gera sql/002_catalogo_atividades.sql a partir dos dados do site (lições, quizzes, minigames).
// Uso: node tools/gerar_catalogo.js
const path = require('path'), fs = require('fs');
const root = path.join(__dirname, '..');
const CL = require('./_load.js')(['lessons-1', 'lessons-2', 'quizzes', 'games'].map(f => path.join(root, 'assets/js/data', f + '.js')));
const rows = [];
CL.data.lessons.forEach(l => rows.push([`lesson-${l.id}`, 'lesson', 30]));
Object.entries(CL.data.quizzes).forEach(([k, q]) => {
  q.questions.forEach(x => rows.push([x.id, 'quiz', q.xp]));
  rows.push([`quiz-${k}-done`, 'quiz-bonus', q.bonus]);
});
CL.data.games.forEach(g => rows.push([`game-${g.slug}`, 'game', g.xp]));
const sql = `-- Catálogo de atividades (GERADO por tools/gerar_catalogo.js; pode ser executado várias vezes)
-- Tarefas diárias não entram aqui: a função award_xp trata o padrão daily-AAAA-MM-DD-N.
insert into public.activity_catalog (id, kind, xp) values
${rows.map(r => `  ('${r[0]}', '${r[1]}', ${r[2]})`).join(',\n')}
on conflict (id) do update set kind = excluded.kind, xp = excluded.xp;
`;
fs.writeFileSync(path.join(root, 'sql/002_catalogo_atividades.sql'), sql);
console.log(rows.length + ' atividades no catálogo');
