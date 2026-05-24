<%*
const today = tp.date.now("YYYY-MM-DD");

async function choose(label, choices, fallback) {
  const value = await tp.system.suggester(choices, choices, false, label);
  return value || fallback;
}

const type = await choose("Type", ["low task", "task"], "low task");
const statut = await choose("Statut", ["A faire", "En cours", "Fait", "Trash"], "A faire");
const priorite = await choose("Priorite", ["P1", "P2", "P3"], "P1");
const niveau = await choose("Niveau", ["facile", "difficile"], "facile");

const categoryChoices = ["DashBoard User", "Dashboard Admin", "FrontEnd", "BackEnd", "Design"];
const categories = [];

while (true) {
  const label = categories.length === 0 ? "Categorie" : "Ajouter une autre categorie ou terminer";
  const choice = await tp.system.suggester(
    [...categoryChoices, "Terminer"],
    [...categoryChoices, "__done__"],
    false,
    label
  );

  if (!choice || choice === "__done__") break;
  if (!categories.includes(choice)) categories.push(choice);
}

if (categories.length === 0) categories.push("BackEnd");

const categorieYaml = categories.length === 1
  ? categories[0]
  : `\n${categories.map((category) => `  - ${category}`).join("\n")}`;

tR += `---
type: ${type}
statut: ${statut}
categorie: ${categorieYaml}
priorite: ${priorite}
Niveau: ${niveau}
created_at: ${today}
updated_at: ${today}
---

# ${tp.file.title}
`;
-%>
