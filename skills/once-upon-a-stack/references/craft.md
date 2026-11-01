# Craft

## Files

```
<library>/<slug>--<topic>/     For example: the-squirrels-pantry--caching
  index.html             The finished book, generated. Never edit by hand.
  .source/
    book.json            Title, style, cast, sources, rewrites
    chain.json           Each chapter's goal, and each attempt, break and arrival
    plan.md              Approved contents and progress, for resuming
    symbols.svg          <symbol> art and optional filters. No <svg>/<defs> wrapper.
    book.css             Optional: world colors and scene motion. Page sizing and reference pages come from the shell.
    book.js              Optional: page-specific behavior, runs after the shell
    pages/NN-name.html   One <section class="page ..."> per file, sorted by name
    facts/NN-journey.md  Research dossiers
```

`assets/example/` is the `.source` of a complete, fact-checked book about caching in the mid-century style: `book.json`, `chain.json`, `symbols.svg` and `pages/`. Read it as a guide to the chain, the macros, scenes, journeys and the reference pages. Take each new book's art direction from `references/styles.md`, not from the example.

`book.json`:
```json
{
  "title": "The Busy Harbor",
  "slug": "the-busy-harbor",
  "topic": "Kubernetes",
  "style": "cut-paper",
  "written": "2026-10-31",
  "sources": ["kubernetes @ v1.31.0"],
  "rewrites": [{"chapter": "The Night Shift", "date": "2026-11-20", "sources": "kubernetes @ v1.32.0"}],
  "spine": {"bg": "#0F4C4A", "fg": "#F6B01E"},
  "cast": [{"name": "Percy", "real": "the scheduler"}]
}
```

`topic` is the plain name someone would search for. The build requires the folder to be `<slug>--<topic in kebab case>`, such as `the-busy-harbor--kubernetes`. It shows the readable topic in the browser tab, on the cover stamp and on the shelf.

`chain.json`, approved with the table of contents (the first two chapters of the example):
```json
{
  "opening": "Rosie",
  "chapters": [
    {
      "goal": "Rosie wants her slice of pie quickly",
      "from": "start",
      "met": "hit-miss",
      "links": [
        {
          "attempt": "Every slice is ordered from the farm",
          "breaks": "Each read is a slow database trip, and repeated reads of the same hot data overload it",
          "evidence": "Verified",
          "source": "Nishtala et al. NSDI 2013 s2, s3.2, s3.3",
          "arrives": "Della",
          "page": "p-della"
        }
      ]
    },
    {
      "goal": "Rosie wants today's pie, not last week's",
      "from": "price: the case keeps showing a pie after the farm changes the recipe",
      "met": "right-pie",
      "links": [
        {
          "attempt": "A date sticker (TTL) on each pie",
          "breaks": "Short TTL means constant refills and load; long TTL means long staleness",
          "evidence": "Inferred",
          "arrives": null,
          "page": "date-sticker"
        }
      ]
    }
  ]
}
```
- `goal` is what the hero wants, from their side. `from` is `start` for the first chapter, then `price: <the new problem the last fix created>` or `next want: <why the met goal isn't enough>`.
- `met` is the id of the page where the goal is met, after the chapter's links and before the next chapter's.
- `evidence` is `Verified` (needs `source`) or `Inferred`. A break that can't be supported doesn't belong in the chain.
- `arrives` is a cast name, or `null` for a dead end. `page` is the id of the page where that link plays out.

The build enforces the chapters. Each needs a goal, at least one link, a valid `from` and a `met` page, and the hero must be named both at the chapter's start (up to its first link page) and on its `met` page. Every cast member must be `opening` or arrive in exactly one link, and link pages must run in reading order. No name may appear before the page where the character arrives. One page must have the class `full-picture`, after every arrival and naming every character, and cast cards appear only there or later.

## Macros (expanded by the build)

| Write | Result |
|---|---|
| `[[Hazel|the cache]]` | Hazel *(the cache)* in the quiet label style. In `book.js`, only inside single-quoted strings. |
| `{{tag|cx|top|Name|function}}` | A name tag in the book's style in an SVG scene, centered at `cx`, about 54 units tall |
| `{{title-scraps}}` | The title as individual letters in the book's style |
| `{{stamp}}` | The cover stamp with date, sources and rewrites |

The build fails when a cast name in story text has no label. Give `class="plain"` to pages that introduce names some other way (cover, cast, glossary).

## Page building blocks

Every page: `<section class="page p-c" id="unique-id" aria-labelledby="heading-id" tabindex="-1">`. Backgrounds: `p-a`, `p-b`, `p-c`. Add the `hidden` attribute to all but the first page. The heading text becomes the page's name in the menus.

| Need | Markup |
|---|---|
| Art and text side by side | `<div class="scroller"><div class="leaf"><div class="art">svg</div><div class="sheet">text</div></div></div>` |
| Art above text | Add `stack` to `.leaf` |
| Chapter name | `<p class="running">Chapter title</p>` first in `.sheet`. Consecutive pages sharing it are grouped in the menus. |
| Grown-ups notes | `<div class="note-src">` as a direct child of the page. Open with `<h3>For grown-ups</h3>`. |
| Evidence label | `<span class="b v">Verified</span>`, `b i` Inferred, `b u` Unknown |
| Citation | `<p class="src">repo, file, function @ commit</p>` |
| Scene origin | `<p class="origin">This really happened: INC-123</p>` or `Imagine if` |
| What people see | `<p class="seen">` |
| Before and after | `<div class="compare">` with two SVGs (second inside `.with`), `.tagline.left`, `.tagline.right`, `<input type="range" min="0" max="100" value="50" aria-label="...">`, `<div class="bar"><div class="knob" aria-hidden="true">&#8596;</div></div>` |
| Step-through journey | `<div class="journey">` containing the SVG and `<ol class="steps"><li>...</li></ol>`. Inside the SVG: `data-show="2 3"` shows an element on those steps, and `data-move='{"1":"translate(0px,0px)","3":"translate(400px,0px)"}'` moves it. The shell adds the buttons. |
| A play you trigger | `<button data-play>` plus your own code in `book.js` |
| Speech | `<p class="bubble">` |
| Recap | `<div class="recap">` |
| Quiz | `<details class="quiz"><summary>Question</summary>Answer</details>` |
| Full picture | `<section class="page p-b plain full-picture" ...>`: the hero's last trip as one scene. Cast cards may follow on it or on the next page. |
| Cast card, full picture only | `<article class="scrap" style="--c:#FFD9A0">`. Add `villain` for torn dark paper. Wrap in `.cast-grid`, inside `.cast-wrap`. |
| Reference page | `<div class="scroller"><div class="ref"><div class="sheet">`. Use `<div class="cols">` of `<p>` for two-column lists (unknowns, glossary) and a `<table>` for the debugging index. The shell styles both. |
| Link to a page | `<a href="#" data-goto="page-id">` |

## Art

Follow `references/styles.md`. Draw in hand-written SVG from simple shapes, and reuse one set of `<symbol>`s so characters stay identical across pages.

- Scenes use `viewBox="0 0 1000 460"` unless they need otherwise, with a reusable backdrop symbol.
- `book.css` may fine-tune colors and add scene motion, but the style sets the look.

## Motion

- **Triggered by the reader:** can be expressive, like a walk across the valley after pressing a button.
- **Runs on its own:** slow and small, enough to ignore. Use the shell's `.bob`, `.flap`, `.wander`. Cycles of 3 seconds or more, and movement within about 15 units.
- **Plays once on opening a page:** short and purposeful, like a swoop or cards landing.
- **Page turns:** the shell's quarter-second nudge. No full-page swings.

Only animate inside `.active` pages. Don't combine an attribute `transform` with a CSS transform on one element: wrap it in a `<g>`. To flip a moving character, flip an inner group and keep its tag outside, so text never mirrors. Respect reduced motion: the shell stops CSS animation, and any `book.js` play must still reach its final state and caption.

## Layout

The shell shows a "who's here so far" strip above the bottom bar on story pages, generated from `chain.json`. Don't draw your own.

Laptop first, around 1366x768. Each page should fit without scrolling. Inner scrolling is only a fallback for small screens. Keep name tags clear of each other and of faces.
