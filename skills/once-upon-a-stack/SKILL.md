---
name: once-upon-a-stack
description: Use when the user asks to build, write or rewrite a book, picture book, storybook or children's-book explanation of any topic (your company's architecture, React internals, Kubernetes, Grafana, a concept), asks to add to or change a book in the library, or wants a topic explained deeply as a story to keep and reread.
compatibility: Works with any agent that reads Agent Skills. Needs Python 3, Node.js 22+ and a Chromium-based browser (Chrome, Chromium, Edge or Brave).
---

# Once Upon a Stack

A book explains one topic deeply as a children's story with real engineering underneath. It is one self-contained offline HTML file in `<library>/<slug>--<topic>/index.html`, listed on the shelf at `<library>/index.html`. Reading it needs no agent and no network. It changes only when the user asks for a rewrite.

The folder always says what the book is about, in kebab case: the story name, a double hyphen, then the real topic, such as `the-diner-on-long-road--caching`. Below, `<book>` means that folder.

Paths below are relative to this skill's directory.

## If your agent can't do something

- **No subagents:** research the journeys one at a time yourself, writing each dossier before starting the next. For the fact-check, ask the user to run it in a new session with the brief in `references/research.md`, so the checker still didn't write the book.
- **Can't view images:** rely on the check's report, and ask the user to open the screenshots in `.source/check/` and tell you what looks wrong.

## Check the tools

Do this first, every time, before any research. It takes a few seconds.

1. `python3 --version` (on Windows, `python --version`) must print Python 3.
2. `node scripts/check.mjs --preflight` must print `Ready:`. It confirms Node.js 22 or newer and that a Chromium-based browser (Chrome, Chromium, Edge or Brave) launches.

If either fails, stop. Tell the user exactly what's missing and how to get it: Python from python.org, Node.js from nodejs.org, or a browser. If a browser is installed but not found, set `CHROME_PATH` to its executable. Don't start research until both pass.

## Find the library

Do this next, every time. `<library>` is the `library` value in `~/.config/once-upon-a-stack/config.json`. If that file doesn't exist, ask where to keep the books, suggest `~/once-upon-a-shelf`, and save the folder they choose, for example `{"library": "~/once-upon-a-shelf"}`, creating the folders. Ask only once. Don't suggest `~/Library` or `~/library`: on macOS that is a hidden system folder.

## Build a new book

1. **Scope.** Do a quick map pass of the topic: what exists, who talks to whom, and which problem forced each part to exist. Choose a world that does some of the explaining (`references/story.md`) and an art style that suits it (`references/styles.md`).
2. **Table of contents: the only stop.** Show the world, art style, and the chapters from `references/story.md`. Show the cast, one line per character with the one real thing it maps to, such as `Pip: the request`. For each chapter: its goal, what it comes from (the price or the next want), each attempt, why it breaks (marked Verified with its source, or Inferred) and who arrives, and where the goal is met. Also show what's left out and a rough size. Aim for 20-35 pages unless the user asks for more, and offer a bigger version as an option. Give a rough time for each step and in total, per Progress below. Before showing it, check that every character arrives from a break and maps to one real thing, every break is marked Verified with a source or Inferred, and every chapter's "from" works as one sentence ("Because X, the hero now wants Y"). Fix what fails, then show it. Wait for the user's approval. Adjust and re-show until they approve. Approval covers everything through step 8.
3. **Set up** `<library>/<book>/.source/` as described in `references/craft.md`. Save the approved plan in `plan.md` and the chain in `chain.json`. Every later step updates `plan.md`, with its start and finish time, so an interrupted build can resume from it.
4. **Research** each chapter per `references/research.md`, using one subagent per journey in parallel. Each writes its dossier to `.source/facts/`. Read the dossiers yourself and chase anything thin.
5. **Write and draw** the pages per `references/story.md`, `references/craft.md` and `references/styles.md`. Write the story and art yourself, not through subagents, so voice and characters stay consistent.
6. **Build:** `python3 scripts/build.py "<library>/<book>"` (on Windows, `python`). Fix everything it reports.
7. **Check it visually, headless:** `node scripts/check.mjs "<library>/<book>"`. Read the report and look at every screenshot. Fix, rebuild and re-check until clean. Open a visible browser only for something headless can't settle. Then audit the story: walk `chain.json` against the pages and confirm that each break is shown, each character arrives because of the break before it, and each chapter's goal is met with the hero there. Say each chapter boundary aloud as one sentence ("Because X, the hero now wants Y"). If it only works as "and also", it's a side topic: move it to a "Wait, how?" page or the reference pages. Confirm the full picture shows the hero's last trip as a scene.
8. **Fact-check** with a fresh subagent that didn't write the book, using the brief in `references/research.md`. It checks every claim in the story text, the notes and the scene labels against its cited source. Fix or relabel everything it reports, then rebuild and re-check.
9. **Hand over** the path, the open command, and what's weakest: thin chapters, the count of unknowns, and anything the fact-check couldn't settle. Stop there. Publishing or committing needs its own request.

## Progress

At the start of each step, and after each chapter while writing, post one line with the step, what's done and the time left, such as `Step 5 of 9: writing pages (12 of 30 done), about 10 min left.`

Rough times for a 30-page book, measured on a real run: research 5-10 min, writing 10-20 min, build and visual check 5-10 min, fact-check 10-15 min and fixes about 5 min, so 35-60 min in total. Scale with the page count. Without subagents, research takes about this long for each chapter. Once a step has finished, base the time left on how long the steps so far really took.

## Rewrite

- **Whole book:** repeat steps 1-9. Keep the world, cast and art style unless the user asks otherwise.
- **One chapter or topic:** read `plan.md`, `book.json` and that chapter's dossier. Re-research against current sources, update that part of `chain.json`, rewrite only those pages, and add an entry to `rewrites` in `book.json` so the cover shows that chapter's own date. Then build, check and fact-check those pages. No table of contents approval is needed.
- **Resume:** when `.source/plan.md` shows unfinished work, continue from there.

## Requirements every book meets

- **Everything is explained.** Each character, method and step says what problem it solves and what happens without it. Follow every "wait, how?" until it has a source or is logged as unknown.
- **The story is a series of goals, linked by cause and effect.** Each chapter opens on something the hero wants, caused by the chapter before. Each attempt breaks for a real engineering reason, and each break brings the next character. The cast and whole path appear only near the end. The build enforces this from `chain.json`.
- **Whole-topic stories.** The book teaches the topic. Don't build it around one incident from the conversation unless asked.
- **Nothing is stated beyond its evidence.** Verified, inferred and unknown are labeled, and sources are cited. Unknowns go on the "What we don't know yet" page.
- **The real name stays next to the story name.** Use the `[[Hazel|the cache]]` macro for every mention and `{{tag|...}}` tags in every scene. The build fails on an unlabeled name.
- **Motion stays out of the way, and pages fit a laptop screen.** See `references/craft.md`.

## Common mistakes

| Mistake | Instead |
|---|---|
| Answering from a KB, docs summary or memory | Trace it in the primary source. Facts taken from summaries are often wrong once the code or spec is read. |
| Splitting chapters by repo or module | Split by journey, because bugs live between components |
| Explaining the trip without the need | Start from the tempting wrong answer and show why it breaks |
| Opening with a cast page or system map | Characters arrive one by one, and the full picture comes last |
| Checking only that facts are right | Also check that each character is caused by the failure before it |
| The goal is met early and the book turns into a manual | Give each chapter its own goal, caused by the chapter before, so no stretch of pages runs without one. |
| A table of fields, codes or types as a story page | Put it on the reference pages, or a "Wait, how?" page starting from something the hero holds |
| A villain for every problem | Personify only what recurs or seems to have a will of its own |
| Fast, large ambient animation | Slow and small, so it never pulls the eye from the text. |
| Declaring it done from a passing build | Look at the screenshots |
| The writer checking their own facts | A fresh subagent fact-checks. Writers miss their own overstatements. |
| A long scrolling chapter | One idea per page |
