# Usage : python3 -I outils/index.py <dossier du dépôt>
# Écrit le README racine du dépôt archives-coupes à partir de .index.json (sortie de archive.py).
import sys, os, json
R = sys.argv[1]
idx = json.load(open(os.path.join(R, "outils", "index.json")))
def size(n): return f"{n/1048576:.1f} Mo" if n >= 1048576 else f"{max(1, n//1024)} Ko"
tot = sum(r[5] for r in idx)
out = ["# Archives des coupes de robotique", "",
"Archive des éditions de la Coupe de France de Robotique / Eurobot : règlements, plans, vinyles, modèles 3D,",
"images et texte des pages de présentation. Le but : garder une copie au cas où les sources disparaissent.", "",
"Chaque dossier `<année>-<thème>` contient un `README.md` (fichiers, origine, empreinte SHA-256, texte de la page source),",
"un dossier `fichiers/` et un dossier `images/`.", "",
"## Éditions", "",
"| Édition | Thème | Fichiers | Images | Taille |", "|---|---|---|---|---|"]
for folder, year, theme, nf, ni, b in idx:
    out.append(f"| [{year}]({folder}/) | {theme} | {nf} | {ni} | {size(b)} |")
out += ["", f"Total : {size(tot)}.", "",
"## Sources", "",
"- [PM-ROBOTIX, les tables de jeux](https://www.pm-robotix.eu/accueil/les-tables-de-jeux/) : 1994 à 2025, fichiers sur leur site et leur Google Drive.",
"- [Eurobot](https://www.eurobot.org/) et [Coupe de France de Robotique](https://www.coupederobotique.fr/) : règlements officiels 2026 et 2027.", "",
"## Droits", "",
"Le texte cité des pages sources est repris tel quel. Les documents restent la propriété de leurs auteurs : Planète Sciences, Eurobot, PM-ROBOTIX.",
"Ce dépôt ne fait que les conserver, avec un lien vers leur origine.", "",
"## Outils", "",
"`outils/archive.py` refait l'archive à partir des pages HTML sauvegardées dans `sources/pm-robotix/`, `outils/index.py` régénère ce README.", ""]
open(os.path.join(R, "README.md"), "w").write("\n".join(out))
