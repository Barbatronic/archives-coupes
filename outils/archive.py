# Archive les éditions de la Coupe de France de Robotique dans un dossier par année.
# Usage : python3 -I outils/archive.py sources/pm-robotix . [dossier...]   (dossiers optionnels : limiter à quelques éditions)
# Sources : pages pm-robotix (texte, images, fichiers liés, Google Drive) + fichiers officiels eurobot.org.
import sys, os, re, html, json, hashlib, urllib.request, urllib.parse, datetime
from html.parser import HTMLParser

PAGES, OUT = sys.argv[1], sys.argv[2]
UA = {"User-Agent": "Mozilla/5.0"}
TODAY = datetime.date.today().isoformat()

# dossier -> (titre, thème, pages pm-robotix)
P = "accueil__les-tables-de-jeux__"
YEARS = {
 "1994-sumo": ("1994", "Sumo", [P+"1994-sumo"]),
 "1995-balloon-attack": ("1995", "Balloon Attack", [P+"1995-balloon-attack"]),
 "1996-gold-rush": ("1996", "Gold Rush", [P+"1996-gold-rush"]),
 "1997-basket-ball": ("1997", "Basket-ball", [P+"1997-basket-ball"]),
 "1998-le-football": ("1998", "Le football", [P+"1998-le-football"]),
 "1999-castles": ("1999", "Castles", [P+"1999-castles"]),
 "2000-la-fete-foraine": ("2000", "La fête foraine", [P+"2000-la-fete-foraine"]),
 "2001-l-odyssee-de-l-espace": ("2001", "L'odyssée de l'espace", [P+"2001-lodyssee-de-lespace-esial"]),
 "2002-le-billard-aerien": ("2002", "Le billard aérien", [P+"2002-le-billard-aerien-esial"]),
 "2003-pile-ou-face": ("2003", "Pile ou face", [P+"2003-pile-ou-face"]),
 "2004-coconut-rugby": ("2004", "Coconut Rugby", [P+"2004-coconut-rugby"]),
 "2005-le-bowling": ("2005", "Le bowling", [P+"2005-le-bowling"]),
 "2006-funny-golf": ("2006", "Funny Golf", [P+"2006-funny-golf"]),
 "2007-robot-tri-party": ("2007", "Robot Tri Party", [P+"2007-robot-tri-party"]),
 "2008-mission-to-mars": ("2008", "Mission to Mars", [P+"2008-mission-to-mars"]),
 "2009-temples-en-atlantide": ("2009", "Temples en Atlantide", [P+"2009-temples-en-atlantide"]),
 "2010-feed-the-world": ("2010", "Feed the World", [P+"2010-feed-the-world"]),
 "2011-chess-up": ("2011", "Chess'Up", [P+"2011-chess-up"]),
 "2012-treasure-island": ("2012", "Treasure Island", [P+"2012-treasure-island"]),
 "2013-happy-birthday": ("2013", "Happy Birthday", [P+"2013-happy-birthday"]),
 "2014-prehistobot": ("2014", "Prehistobot", [P+"2014-prehistobot"]),
 "2015-robomovies": ("2015", "Robomovies", [P+"2015-robomovies"]),
 "2016-the-beachbots": ("2016", "The Beachbots", [P+"2016-the-beachbots"]),
 "2017-moon-village": ("2017", "Moon Village", [P+"2017-moon-village", P+"2017-moon-village__coupe-de-belgique-2017", P+"2017-moon-village__coupe-de-france-2017"]),
 "2018-robot-cities": ("2018", "Robot Cities", [P+"2018-robot-cities", P+"2018-robot-cities__coupe-de-belgique-2018", P+"2018-robot-cities__coupe-de-france-2018", P+"2018-robot-cities__toulouse-robot-race-2018"]),
 "2019-atom-factory": ("2019", "Atom Factory", [P+"2019-atom-factory", P+"2019-atom-factory__2019-le-reglement", P+"2019-atom-factory__2019-aire-de-jeu", P+"2019-atom-factory__2019-aire-de-jeu-en-3d", P+"2019-atom-factory__2019-le-comptage-des-points", P+"2019-atom-factory__2019-les-plans"]),
 "2020-sail-the-world": ("2020", "Sail the World", [P+"cdr2020-sail-the-world"]),
 "2021-sail-the-world": ("2021", "Sail the World", [P+"cdr2021-sailtheworld", P+"cdr2021-sailtheworld__2021-laire-de-jeu", P+"cdr2021-sailtheworld__2021-calcul-des-points", P+"cdr2021-sailtheworld__2021-les-plans", P+"cdr2021-sailtheworld__2021-vinyle-pm-robotix"]),
 "2022-age-of-bots": ("2022", "Age of Bots", [P+"cdr2022-ageofbots", P+"cdr2022-ageofbots__2022-laire-de-jeu", P+"cdr2022-ageofbots__vinyle-et-plans"]),
 "2023-the-cherry-on-the-cake": ("2023", "The Cherry on the Cake", [P+"cdr2023-thecherryonthecake", P+"cdr2023-thecherryonthecake__2023-vinyle-pm-robotix"]),
 "2024-farming-mars": ("2024", "Farming Mars", [P+"2024-farming-mars"]),
 "2025-the-show-must-go-on": ("2025", "The Show Must Go On", [P+"2025-the-show-must-go-on"]),
 "2026-winter-is-coming": ("2026", "Winter is Coming", []),
 "2027-the-legend-of-camelot": ("2027", "The Legend of Camelot", []),
}
# Fichiers officiels absents de pm-robotix (pages eurobot.org / coupederobotique.fr de l'édition).
EU = "https://www.eurobot.org/wp-content/uploads/"
EXTRA = {
 "2026-winter-is-coming": ("https://www.eurobot.org/eurobot-contest/eurobot-2026/", [
   EU+"2025/10/Eurobot2026_Rules_1.0_FR.pdf", EU+"2025/10/Eurobot2026_Rules_1.0_EN.pdf", EU+"2025/10/Eurobot2026_Rules_1.0_SP.pdf",
   EU+"2025/09/Eurobot_General_Rules_1.2_FR.pdf", EU+"2025/09/Eurobot_General_Rules_1.2_EN.pdf", EU+"2025/10/Eurobot_General_Rules_1.2_SP.pdf",
   EU+"2025/10/FINAL_1.0_playmat.zip", EU+"2026/05/E2026_Memento_Homologuation_FR.pdf", EU+"2026/05/E2026_Memento_Homologuation_EN.pdf"]),
 "2027-the-legend-of-camelot": ("https://www.coupederobotique.fr/edition-2027/reglement-2027/", [
   EU+"2026/10/Eurobot2027_Rules_FR.pdf", EU+"2026/10/Eurobot2027_Rules_EN.pdf", EU+"2026/10/Eurobot2027_Rules_ES.pdf",
   EU+"2026/10/Eurobot_General_Rules_SR_FR.pdf", EU+"2026/10/Eurobot_General_Rules_SR_EN.pdf", EU+"2026/10/Eurobot_General_Rules_SR_ES.pdf",
   EU+"2026/10/Eurobot_General_Rules_JR_FR.pdf", EU+"2026/10/playmat.zip",
   "https://www.coupederobotique.fr/wp-content/uploads/Eurobot_FR_achat_tapis.pdf"]),
}
FILE_RE = re.compile(r"\.(pdf|zip|rar|7z|step|stp|iges|igs|stl|f3d|f3z|dxf|svg)(\?|$)", re.I)

class Content(HTMLParser):
    """Texte Markdown, images et liens de l'<article> d'une page WordPress, menu latéral exclu."""
    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.depth = 0; s.on = False; s.md = []; s.line = ""; s.href = None; s.atext = ""
        s.imgs = []; s.links = []; s.skip = 0; s.title = ""; s.in_h1 = False; s.side = 0
    def flush(s, prefix=""):
        t = " ".join(s.line.split())
        if t: s.md.append(prefix + t)
        s.line = ""
    def handle_starttag(s, t, a):
        a = dict(a)
        if t == "h1" and "hestia-title" in (a.get("class") or ""): s.in_h1 = True
        if not s.on:
            if t == "article": s.on = True
            return
        if s.side:
            if t == "div": s.side += 1
            return
        if t == "div" and "blog-sidebar-wrapper" in (a.get("class") or ""): s.side = 1; return
        if t == "iframe":
            v = a.get("src") or a.get("data-src") or ""
            if "youtu" in v: s.flush(); s.md.append(f"Vidéo : {v.split('?')[0]}")
        if t in ("script", "style", "iframe"): s.skip += 1
        if t in ("p", "div", "li", "h2", "h3", "h4", "h5", "tr", "figcaption", "br"): s.flush()
        if t == "li": s.line = "- "
        if t in ("h2", "h3", "h4", "h5"): s.line = "#" * (int(t[1]) + 1) + " "
        if t == "a" and a.get("href"): s.href = a["href"]; s.atext = ""
        if t == "img":
            src = a.get("data-orig-file") or a.get("src") or ""
            src = re.sub(r"-\d+x\d+(\.\w+)$", r"\1", src.split("?")[0])
            if "wp-content/uploads" in src: s.imgs.append(src)
    def handle_endtag(s, t):
        if t == "h1": s.in_h1 = False
        if not s.on: return
        if s.side:
            if t == "div": s.side -= 1
            return
        if t == "article": s.flush(); s.on = False; return
        if t in ("script", "style", "iframe"): s.skip = max(0, s.skip - 1)
        if t == "a" and s.href is not None:
            txt = " ".join(s.atext.split())
            s.links.append((s.href, txt))
            if txt: s.line = s.line[: len(s.line) - len(s.atext)] + f"[{txt}]({s.href})"
            s.href = None
        if t in ("p", "li", "h2", "h3", "h4", "h5", "tr", "figcaption"): s.flush()
    def handle_data(s, d):
        if s.in_h1: s.title += d
        if not s.on or s.skip or s.side: return
        s.line += d
        if s.href is not None: s.atext += d

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read(), r.headers

def drive_id(u):
    m = re.search(r"drive\.google\.com/(?:file/d/|open\?id=)([\w-]{20,})", html.unescape(u))
    return m.group(1) if m else None

def download(url, dest_dir, used):
    """Télécharge `url` dans dest_dir. Retourne (nom, octets, sha256) ou None si ce n'est pas un fichier."""
    did = drive_id(url)
    real = f"https://drive.usercontent.google.com/download?id={did}&export=download&confirm=t" if did else url
    data, h = fetch(real)
    ctype = (h.get("Content-Type") or "").split(";")[0]
    if ctype == "text/html": return None
    m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', h.get("Content-Disposition") or "")
    name = urllib.parse.unquote(m.group(1)) if m else urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(url).path))
    name = re.sub(r"[^\w.\-]+", "_", name) or (did or "fichier")
    base, ext = os.path.splitext(name); n = 2
    while name in used: name = f"{base}-{n}{ext}"; n += 1
    used.add(name)
    os.makedirs(dest_dir, exist_ok=True)
    open(os.path.join(dest_dir, name), "wb").write(data)
    return name, len(data), hashlib.sha256(data).hexdigest()

def size(n): return f"{n/1048576:.1f} Mo" if n >= 1048576 else f"{max(1, n//1024)} Ko"

index = []; log = []
only = set(sys.argv[3:])
for folder, (year, theme, pages) in YEARS.items():
    if only and folder not in only: continue
    d = os.path.join(OUT, folder); os.makedirs(d, exist_ok=True)
    texts, files, imgs, seen = [], [], [], set()
    used_f, used_i = set(), set()
    targets = []   # (url, page source)
    for p in pages:
        c = Content(); c.feed(open(os.path.join(PAGES, p + ".html"), errors="ignore").read())
        src = "https://www.pm-robotix.eu/" + p.replace("__", "/") + "/"
        texts.append((c.title.strip() or p, src, re.sub(r"(?m)^(- .*)\n\n(?=- )", r"\1\n", "\n\n".join(c.md))))
        for u in c.imgs: targets.append((u, src, "img"))
        for u, _ in c.links:
            u = html.unescape(u)
            if drive_id(u) or FILE_RE.search(u): targets.append((u, src, "file"))
    if folder in EXTRA:
        src, urls = EXTRA[folder]
        for u in urls: targets.append((u, src, "file"))
    for u, src, kind in targets:
        key = drive_id(u) or u
        if key in seen: continue
        seen.add(key)
        try:
            r = download(u, os.path.join(d, "images" if kind == "img" else "fichiers"), used_i if kind == "img" else used_f)
        except Exception as e:
            log.append(f"{folder}\tECHEC\t{u}\t{e}"); continue
        if not r: log.append(f"{folder}\tHTML\t{u}"); continue
        (imgs if kind == "img" else files).append((r, u, src))
    # README de l'édition
    out = [f"# {year} : {theme}", "",
           f"Archive de l'édition {year} de la Coupe de France de Robotique / Eurobot, faite le {TODAY}.",
           "Les documents restent la propriété de leurs auteurs (Planète Sciences, Eurobot, PM-ROBOTIX).", ""]
    if files:
        out += ["## Fichiers", "", "| Fichier | Taille | Origine | SHA-256 |", "|---|---|---|---|"]
        for (n, b, h), u, src in files:
            out.append(f"| [{n}](fichiers/{n}) | {size(b)} | [lien]({u}) | `{h[:16]}` |")
        out.append("")
    if imgs:
        out += ["## Images", "", f"{len(imgs)} images dans [images/](images/), reprises des pages sources.", ""]
    out += ["## Sources", ""] + [f"- [{t}]({s})" for t, s, _ in texts]
    if folder in EXTRA: out.append(f"- [Page officielle de l'édition]({EXTRA[folder][0]})")
    out.append("")
    for t, s, md in texts:
        if md.strip():
            out += [f"## Texte de la page : {t}", "", f"Source : {s}", "", md, ""]
    open(os.path.join(d, "README.md"), "w").write("\n".join(out))
    tot = sum(r[0][1] for r in files + imgs)
    index.append((folder, year, theme, len(files), len(imgs), tot))
    print(f"{folder}: {len(files)} fichiers, {len(imgs)} images, {size(tot)}", flush=True)

json.dump(index, open(os.path.join(OUT, "outils", "index.json"), "w"), ensure_ascii=False)
open(os.path.join(OUT, ".archive.log"), "w").write("\n".join(log))
print("journal :", len(log), "lignes")
