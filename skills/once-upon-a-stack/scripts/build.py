#!/usr/bin/env python3
"""Assemble <book>/.source into one offline index.html and refresh the shelf.

Usage: python3 build.py "<library>/<slug>--<topic>"
Exits 1 and writes nothing if the book has problems.
"""
import base64
import html
import json
import re
import subprocess
import sys
import tempfile
import urllib.parse
import xml.dom.minidom as minidom
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets"
STYLES = ASSETS / "styles"
DEFAULT_STYLE = "cut-paper"


def font_css(style_id):
    folder = STYLES / style_id
    rules = []
    for family, weight, style, name in json.loads((folder / "style.json").read_text(encoding="utf-8"))["fonts"]:
        data = base64.b64encode((folder / "fonts" / name).read_bytes()).decode()
        rules.append(
            f'@font-face{{font-family:"{family}";font-weight:{weight};font-style:{style};'
            f'src:url(data:font/woff2;base64,{data}) format("woff2");font-display:swap}}'
        )
    return "\n".join(rules)


def tag(match):
    cx, top = int(match[1]), int(match[2])
    name, func = html.escape(match[3]), html.escape(f"({match[4]})")
    width = max(len(match[3]) * 12.5, (len(match[4]) + 2) * 9.8) + 26
    return (
        f'<g class="ntag" transform="rotate(-1.2 {cx} {top + 26})">'
        f'<rect x="{round(cx - width / 2)}" y="{top}" width="{round(width)}" height="54"/>'
        f'<text class="nt-n" x="{cx}" y="{top + 23}">{name}</text>'
        f'<text class="nt-f" x="{cx}" y="{top + 45}">{func}</text></g>'
    )


def title_scraps(title):
    words = []
    for word in title.split():
        letters = "".join(f'<span class="l">{html.escape(c)}</span>' for c in word)
        words.append(f'<span class="word" aria-hidden="true">{letters}</span>')
    return "".join(words)


def stamp(book):
    lines = [
        f"<span><strong>A book about {html.escape(book['topic'])}</strong></span>",
        f"<span>Written {html.escape(book['written'])}</span>",
    ]
    if book.get("sources"):
        lines.append(f"<span>From {html.escape(', '.join(book['sources']))}</span>")
    for r in book.get("rewrites", []):
        extra = f", from {r['sources']}" if r.get("sources") else ""
        lines.append(f"<span>{html.escape(r['chapter'])} rewritten {html.escape(r['date'])}{html.escape(extra)}</span>")
    return f'<p class="stamp">{"".join(lines)}</p>'


def expand(text, book):
    text = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r'\1 <span class="who">(\2)</span>', text)
    text = re.sub(r"\{\{tag\|(-?\d+)\|(-?\d+)\|([^|}]+)\|([^|}]+)\}\}", tag, text)
    text = text.replace("{{title-scraps}}", title_scraps(book["title"]))
    return text.replace("{{stamp}}", stamp(book))


def story_text(page):
    """Visible story text, with labels kept so the name check can see them."""
    body = re.sub(r"<(svg|pre|code)\b.*?</\1>", " ", page, flags=re.S)
    body = re.sub(r'<span class="who">', "", body)
    return html.unescape(re.sub(r"<[^>]+>", " ", body))


def check(book, files, pages, symbols, css, js, problems):
    all_html = symbols + "\n".join(pages)
    for name, page in zip(files, pages):
        if not re.match(r"\s*(<!--.*?-->\s*)?<section\b[^>]*class=\"[^\"]*\bpage\b", page, re.S):
            problems.append(f"{name}: must start with <section class=\"page ...\">")
        heading = re.search(r'aria-labelledby="([^"]+)"', page)
        if not heading:
            problems.append(f"{name}: the section needs aria-labelledby")
        elif f'id="{heading[1]}"' not in page:
            problems.append(f"{name}: no element with id {heading[1]}")
        for svg in re.findall(r"<svg\b.*?</svg>", page, re.S):
            try:
                minidom.parseString(svg)
            except Exception as err:
                problems.append(f"{name}: invalid SVG: {err}")
        if "plain" not in (re.search(r'class="([^"]*)"', page) or [None, ""])[1]:
            text = story_text(page)
            for member in book.get("cast", []):
                for hit in re.finditer(re.escape(member["name"]) + r"\b(?!\s*\()", text):
                    around = " ".join(text[max(0, hit.start() - 30): hit.end() + 25].split())
                    problems.append(f"{name}: unlabeled name, use [[{member['name']}|{member['real']}]]: ...{around}...")
        if "{{" in page:
            problems.append(f"{name}: unexpanded macro: {page[page.index('{{'):][:50]}")
    for i, name in enumerate(files):
        tag_open = re.search(r"<section\b[^>]*>", pages[i])
        if tag_open and (" hidden" in tag_open[0]) != (i != 0):
            problems.append(f"{name}: only the first page goes without the hidden attribute")
    try:
        minidom.parseString(f'<svg xmlns:xlink="x">{symbols}</svg>')
    except Exception as err:
        problems.append(f"symbols.svg: invalid: {err}")
    ids = re.findall(r'\bid="([^"]+)"', all_html)
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append(f"duplicate id: {dup}")
    known = set(ids)
    for ref in sorted(set(re.findall(r'href="#([A-Za-z][^"]*)"', all_html)) - known):
        problems.append(f"href to missing symbol: #{ref}")
    for ref in sorted(set(re.findall(r'data-goto="([^"]+)"', all_html)) - known):
        problems.append(f"data-goto to missing page: {ref}")
    if js.strip():
        with tempfile.NamedTemporaryFile("w", suffix=".js") as temp:
            temp.write(js)
            temp.flush()
            result = subprocess.run(["node", "--check", temp.name], capture_output=True, text=True)
            if result.returncode:
                problems.append(f"book.js: {result.stderr.strip()}")


def check_chain(book, chain, pages, problems):
    """The story is a series of chapter goals: characters arrive because of failures, and the cast comes last."""
    if chain is None:
        problems.append("chain.json is missing. See references/craft.md")
        return []
    cast = {m["name"]: m["real"] for m in book.get("cast", [])}
    for key in ("opening", "chapters"):
        if not chain.get(key):
            problems.append(f"chain.json: {key} is required")
    if not chain.get("chapters") or not chain.get("opening"):
        return []
    page_ids = [(re.search(r'<section\b[^>]*\bid="([^"]+)"', p) or [None, None])[1] for p in pages]
    order = {pid: i for i, pid in enumerate(page_ids) if pid}
    hero = chain["opening"]
    if hero not in cast:
        problems.append(f"chain.json: opening {hero} is not in the book.json cast")
    first_story = next((i for i, p in enumerate(pages) if "plain" not in (re.search(r'class="([^"]*)"', p) or [None, ""])[1]), 0)
    names_hero = lambda i: re.search(re.escape(hero) + r"\b", story_text(pages[i]))
    start, links = first_story, []
    for c, chapter in enumerate(chain["chapters"], 1):
        label = f"chain.json chapter {c}"
        if not chapter.get("goal"):
            problems.append(f"{label}: goal is required")
        source = chapter.get("from", "")
        if c > 1 and not re.match(r"(price|next want):\s*\S", source):
            problems.append(f'{label}: "from" must start with "price:" or "next want:" and say what caused this goal')
        own = chapter.get("links") or []
        if not own:
            problems.append(f"{label}: needs at least one link")
        links += own
        met = order.get(chapter.get("met"))
        if met is None:
            problems.append(f"{label}: no met page with id {chapter.get('met')}")
            continue
        link_pages = [order[l["page"]] for l in own if l.get("page") in order]
        if link_pages and min(link_pages) < start:
            problems.append(f"{label}: its links start before the previous chapter's goal is met")
        if link_pages and met < max(link_pages):
            problems.append(f"{label}: the met page comes before the chapter's links")
        opening_end = min(link_pages) if link_pages else met
        if not any(names_hero(i) for i in range(start, opening_end + 1)):
            problems.append(f"{label}: {hero} isn't named at the chapter's start (pages {start + 1}-{opening_end + 1})")
        if not names_hero(met):
            problems.append(f"{label}: {hero} isn't named on the met page {chapter['met']}")
        start = met + 1
    arrivals = {}
    previous = -1
    for n, link in enumerate(links, 1):
        for key in ("attempt", "breaks", "evidence", "page"):
            if not link.get(key):
                problems.append(f"chain.json link {n}: {key} is required")
        if link.get("evidence") not in ("Verified", "Inferred"):
            problems.append(f"chain.json link {n}: evidence must be Verified or Inferred")
        if link.get("evidence") == "Verified" and not link.get("source"):
            problems.append(f"chain.json link {n}: Verified needs a source")
        where = order.get(link.get("page"))
        if where is None:
            problems.append(f"chain.json link {n}: no page with id {link.get('page')}")
            continue
        if where < previous:
            problems.append(f"chain.json link {n}: pages must run in reading order")
        previous = where
        who = link.get("arrives")
        if who:
            if who not in cast:
                problems.append(f"chain.json link {n}: {who} is not in the book.json cast")
            elif who in arrivals or who == hero:
                problems.append(f"chain.json link {n}: {who} already arrived")
            else:
                arrivals[who] = where
    arrivals = {hero: first_story, **arrivals}
    for name in cast:
        if name not in arrivals:
            problems.append(f"chain.json: {name} never arrives")
    for name, where in arrivals.items():
        for i in range(where):
            visible = story_text(pages[i]) + " ".join(re.findall(r'class="nt-n"[^>]*>([^<]+)<', pages[i]))
            if re.search(re.escape(name) + r"\b", visible):
                problems.append(f"{page_ids[i]}: {name} appears before arriving on page {where + 1}")
    full = [i for i, p in enumerate(pages) if re.search(r'<section\b[^>]*class="[^"]*\bfull-picture\b', p)]
    if len(full) != 1:
        problems.append("exactly one page needs the class full-picture")
    else:
        if full[0] < max(arrivals.values()):
            problems.append("the full-picture page must come after every arrival")
        text = story_text(pages[full[0]])
        for name in cast:
            if not re.search(re.escape(name) + r"\b", text):
                problems.append(f"the full-picture page doesn't name {name}")
        for i in range(full[0]):
            if "cast-grid" in pages[i]:
                problems.append(f"{page_ids[i]}: cast cards belong on the full-picture page")
    return [{"name": n, "real": cast[n], "page": page_ids[arrivals[n]]} for n in sorted(arrivals, key=arrivals.get) if n in cast]


def build_shelf(library):
    fonts = font_css(DEFAULT_STYLE)
    spines = []
    for manifest in sorted(library.glob("*/.source/book.json")):
        book = json.loads(manifest.read_text(encoding="utf-8"))
        folder = manifest.parent.parent
        if not (folder / "index.html").exists():
            continue
        spine = book.get("spine", {})
        spines.append(
            f'<a class="spine" href="{urllib.parse.quote(folder.name)}/index.html" '
            f'style="--bg:{html.escape(spine.get("bg", "#43216B"))};--fg:{html.escape(spine.get("fg", "#F7FBF8"))}">'
            f'<strong>{html.escape(book["title"])}</strong>'
            f'<small class="topic">({html.escape(book.get("topic", ""))})</small>'
            f'<small data-written="{html.escape(book["written"])}">{html.escape(book["written"])}</small></a>'
        )
    shell = (ASSETS / "shelf.html").read_text(encoding="utf-8")
    books = "\n".join(spines) or '<p class="empty">No books yet.</p>'
    (library / "index.html").write_text(shell.replace("{{FONTS}}", fonts).replace("{{BOOKS}}", books), encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    folder = Path(sys.argv[1]).expanduser().resolve()
    source = folder / ".source"
    book = json.loads((source / "book.json").read_text(encoding="utf-8"))
    missing = [k for k in ("title", "slug", "topic", "written") if k not in book]
    if missing:
        sys.exit(f"book.json is missing: {', '.join(missing)}")
    topic_slug = re.sub(r"[^a-z0-9]+", "-", book["topic"].lower()).strip("-")
    expected = f"{book['slug']}--{topic_slug}"
    if folder.name != expected:
        sys.exit(f'The book folder must be named "{expected}", not "{folder.name}"')

    style_id = book.get("style", DEFAULT_STYLE)
    if not (STYLES / style_id / "style.json").exists():
        known = ", ".join(sorted(p.name for p in STYLES.iterdir()))
        sys.exit(f'Unknown style "{style_id}". Available: {known}')

    def optional(name):
        path = source / name
        return path.read_text(encoding="utf-8") if path.exists() else ""

    files = sorted((source / "pages").glob("*.html"))
    if not files:
        sys.exit("No pages in .source/pages")
    pages = [expand(f.read_text(encoding="utf-8"), book) for f in files]
    symbols = expand(optional("symbols.svg"), book)
    css, js = optional("book.css"), expand(optional("book.js"), book)

    problems = []
    chain = json.loads(optional("chain.json")) if optional("chain.json") else None
    arrival_list = check_chain(book, chain, pages, problems)
    check(book, [f.name for f in files], pages, symbols, css, js, problems)
    if problems:
        print(f"{len(problems)} problem(s), nothing written:")
        for problem in problems:
            print(f"- {problem}")
        sys.exit(1)

    shell = (ASSETS / "shell.html").read_text(encoding="utf-8")
    for key, value in {
        "{{TITLE}}": html.escape(f"{book['title']} ({book['topic']})"),
        "{{SLUG}}": book["slug"],
        "{{FONTS}}": font_css(style_id),
        "{{STYLE_DEFS}}": (STYLES / style_id / "defs.svg").read_text(encoding="utf-8"),
        "{{STYLE_CSS}}": (STYLES / style_id / "style.css").read_text(encoding="utf-8"),
        "{{SYMBOLS}}": symbols,
        "{{PAGES}}": "\n".join(pages),
        "{{BOOK_CSS}}": css,
        "{{BOOK_JS}}": js,
        "{{ARRIVALS}}": json.dumps(arrival_list),
    }.items():
        shell = shell.replace(key, value)
    (folder / "index.html").write_text(shell, encoding="utf-8")
    build_shelf(folder.parent)
    size = (folder / "index.html").stat().st_size // 1024
    print(f"Built {folder / 'index.html'}: {len(pages)} pages, {size} KB. Shelf updated.")


if __name__ == "__main__":
    main()
