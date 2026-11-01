# Once Upon a Stack

**Understand any codebase or technical topic properly, as a picture book you keep.**

An Agent Skill for Claude Code, Codex, Cursor, Gemini CLI and GitHub Copilot that turns a topic into an illustrated, interactive visual explainer. Ask your coding agent once, and you get a book about DNS, Kubernetes, React, or your own company's system. It's one HTML file you can open any time, offline, for free, without asking anyone again.

![The cover of The Diner on Long Road](docs/screenshots/cover.png)

## Why

You've probably been here:

- Someone in a meeting says "it's probably a cache stampede", and you nod.
- You've used Kubernetes for two years, and you still couldn't say why a pod needs a service.
- You asked an AI to explain something last month. It was a great answer. Now it's lost somewhere in your chat history, so you ask again.

Most explanations tell you **what** a thing does. They skip **why it has to exist**, and that's the part that makes it stick.

These books start from the why. Someone wants something simple and tries the obvious way. It breaks, for a real engineering reason. A new character shows up with the fix, and the fix misses something. By the last page you've met every part of the system, and you know what would go wrong without each one.

It's written like a children's book on purpose: a children's book can't assume you already know anything. The engineering underneath stays real, and so do the sources.

## When you'd reach for it

- **You just joined a team.** Point it at the codebase and get the story of how a request really travels through your six services. Read it on your first weekend.
- **Something you use every day is still magic.** "How does React decide what to re-render?" Get an answer that isn't another blog post you half remember.
- **It's 2am and the database is on fire.** Every book ends with a debugging index: find what you're seeing, and it takes you to the page that explains it.
- **You have to explain it to someone else.** Send a new hire or your PM one file. They read the story. The engineers open the notes.
- **You've got an interview coming up.** You'll be able to explain why a cache needs an eviction policy, not just that it has one.

## See one

Two books made by this skill, each readable in your browser:

- **[The Diner on Long Road](https://andrewlawendy.github.io/once-upon-a-stack/demo/the-diner-on-long-road.html)**, 23 pages about caching. Rosie wants a slice of pie, but every pie comes from a farm at the end of a long road. A pie case fixes that, until the recipe changes and the case still sells the old one. At noon a popular pie's sticker runs out, two hundred people miss at once, and that real failure gets a villain.
- **[The Pigeons of Two Peaks](https://andrewlawendy.github.io/once-upon-a-stack/demo/the-pigeons-of-two-peaks.html)**, 40 pages about TCP. Juno wants her long story to reach Grandpa across a valley where pigeons get lost, arrive out of order and show up twice. Every part of TCP arrives because the simpler idea broke, including the real 1986 day the internet nearly stopped.

Every character keeps its real job right next to its name, so you never have to remember who's who.

<p>
  <img src="docs/screenshots/rush.png" width="49%" alt="The Rush, a crowd of two hundred orders, jams the road to the farm">
  <img src="docs/screenshots/tcp.png" width="49%" alt="The masked fox guesses the next starting number, from the TCP book">
</p>

For engineers, every page has a "For grown-ups" drawer with the real terms, config and sources. Each claim is marked Verified, Inferred or Unknown.

![The For grown-ups notes, in dark mode](docs/screenshots/notes.png)

## What a book is like

- **Pages, not a long scroll.** Built for a laptop, with light and dark themes and quiet motion.
- **Things you can try.** Step through a journey, or drag a slider to see before and after.
- **Researched, not improvised.** The agent reads the code, specs and papers. What it can't settle goes on a "What we don't know yet" page.
- **Its own look.** Each book picks a style that suits its topic: cut paper, woodcut, mid-century, stained glass, blueprint, vintage poster or pixel art.

## Usage

```
/once-upon-a-stack DNS
/once-upon-a-stack how React decides what to re-render
/once-upon-a-stack rewrite the eviction chapter of The Diner on Long Road
```

The first time you run it, the agent asks where to keep your books and suggests `~/once-upon-a-shelf`. Open `index.html` in that folder to see your shelf: one spine per book with its title, topic and age, and a click opens the book. It updates itself every time a book is built.

![A shelf with five books](docs/screenshots/shelf.png)

1. The agent maps the topic and shows you a table of contents: the world, the art style, and each chapter's goal, attempts, breaks and new characters. This is the only stop. Nothing is built until you approve it.
2. It researches each journey in parallel, writes and draws the pages, builds the book, and checks every page in a headless browser, in light and dark.
3. It hands you the path to the book and says which parts are weakest.

A 30-page book takes about 25-45 minutes, and the agent tells you how far along it is as it goes. A big topic uses a lot of tokens, since it runs several research agents.

## Requirements

- Claude Code, or another coding agent that supports [Agent Skills](https://agentskills.io)
- Python 3
- Node.js 22 or newer
- Google Chrome, Chromium, Edge or Brave, for the visual check. If it isn't found, set `CHROME_PATH` to the browser's executable.

## Install

One command for any agent (Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and more). It asks which agents to install it for:

```
npx skills add AndrewLawendy/once-upon-a-stack -g
```

Or, in Claude Code (2.1.275 or later), as a plugin:

```
/plugin install once-upon-a-stack --marketplace AndrewLawendy/once-upon-a-stack
```

Or by hand: clone the repo and link the skill into your agent's skills folder, `~/.claude/skills` for Claude Code or `~/.agents/skills` for Codex, Gemini CLI, GitHub Copilot and Cursor:

```
git clone https://github.com/AndrewLawendy/once-upon-a-stack.git ~/once-upon-a-stack
ln -s ~/once-upon-a-stack/skills/once-upon-a-stack ~/.claude/skills/once-upon-a-stack
```

In agents other than Claude Code, ask for a book in plain words, such as "make a picture book about DNS". These agents are supported by their documentation but not tested yet. Agents that can't start subagents or view images still work, with a few extra steps the skill explains.

## Status

Work in progress. The visual check is tested on Linux; the macOS and Windows browser paths are written but not yet tested on those systems.

## License

MIT. The bundled fonts keep their own licenses: see [`font-licenses`](skills/once-upon-a-stack/assets/font-licenses).
