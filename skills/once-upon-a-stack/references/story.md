# Story

Write for a curious reader who knows nothing about the topic and refuses to take anything on faith. The story is a series of goals. In each chapter someone wants something, each attempt breaks for a real engineering reason, and each break brings the next character.

## A chapter

1. **Goal.** The chapter opens on something the opening character (the hero) wants, told from their side: "Tam wants the number fast, every time", not "caching". State it plainly.
2. **The tempting first attempt.** The hero tries what a smart beginner would try. This is the reader's own "why can't I just...?", such as "why can't I write www.google.com and find it in one step?".
3. **It breaks.** Show the real reason in a scene, ending with what a person actually sees.
4. **A new character arrives** with a fix, for a reason that makes sense in the world.
5. **The fix misses something.** Go back to step 3.
6. **The goal is met** on the chapter's last page, with the hero there to see it.

Rules for the chain inside a chapter:

- **A character enters only because of a problem.** Each one arrives from the failure just before it. No introductions in advance.
- **Breaks are the real ones.** Each break is a challenge engineers actually faced, and each fix is what actually answers it. Order follows cause and effect, not history. If the real timeline differs, say so in the notes.
- **One fix doesn't always work.** Include real dead ends and real partial fixes. A fix can create the next problem: "every helper invites a new villain".

## From chapter to chapter

**Each goal comes from the chapter before,** in one of two ways:
- **The price:** the last fix created a new problem. The notebook makes forged notes pay off, so "Tam needs to know the number is real".
- **The next want:** the goal was met, and now the hero wants more. "It works, but every visit takes a fifth of a second" leads to "Tam wants it fast".

Say the boundary aloud as one sentence: "Because the notebook makes forgery pay, Tam needs to know the number is real." If it only works as "and also...", the topic is a side topic. Put it on a "Wait, how?" page inside the chapter it belongs to, or on the reference pages. Don't make it a chapter.

**The hero stays the hero.** They appear in every chapter, try the tempting thing, and are there when the goal is met. Other characters do the fixing, but it's the hero's problem they fix. Characters from earlier chapters come back when they're needed.

**Tables don't tell stories.** Lists of fields, codes or types go on the reference pages, or on a "Wait, how?" page that starts from something the hero is holding ("What's written on Tam's note?").

## The full picture

The hero makes the whole journey once more, drawn as one scene, meeting each character in the order the trip reaches them, and arrives at the goal. Villains are shown where they would strike and what stops them. By this point each character has earned their place. The cast cards come after the scene, on the same page or the next, never instead of it.

## World

Give each book a world whose logic explains the topic, and use it consistently:
- Kubernetes: a busy harbor with a harbor master who keeps things running as planned.
- React: a theater, where the director compares the new script with what's on stage and only changes what's different.
- Grafana: a weather station with instruments and a wall of charts.

These are starting points, so pick what explains the topic best.

## Characters

Characters can be anything that suits the world: people, animals, household objects, tools, rivers, weather, buildings. Choose what makes the job obvious at a glance.

Every character maps to one real thing, written in `book.json`, and has a name, one signature color and one job.

Aim for about 10 characters. A mechanism that doesn't recur can be a prop, like a stencil or a bell, rather than a character. A big cast crowds the "So far" strip and is hard to keep straight.

Treat challenges in one of three ways:
- **A character:** only if it keeps coming back or seems to have a will of its own. A villain's appearance still spells out the real mechanism. "The Echo did it" is not a root cause.
- **Weather:** how the world simply is, such as distance, delay or poor phone lines. Nobody's fault.
- **A puzzle:** solved once and stays solved. No villain needed.

Accidental villains are welcome: mistakes of our own, and problems created by an earlier fix.

## Pages

One idea per page, fitting one laptop screen without scrolling. A chain link often takes these pages, and any can be dropped or added when the topic calls for it:

1. **The attempt:** what the character tries, and why it seems reasonable.
2. **Without it:** the scene where it breaks, ending with what a person actually sees. This is the most valued part of the book, so don't reduce it to a one-line statement. Label it "This really happened" or "Imagine if". A before and after slider usually suits it.
3. **The fix:** who arrives and how they help, shown working, as a step-through or play when it has moving parts.
4. **Wait, how?:** the tiny details nobody explains. Give the important ones their own page.
5. **The price:** what the fix costs or misses. This leads straight into the next link.
6. **For grown-ups:** the notes drawer, on every story page. Real names, fields, config and sources, with evidence labels.

End a chapter with a short recap, and a one-question quiz where it adds something.

## Voice

Short sentences and concrete images. Warm and a little funny, without baby talk. The engineering stays exact: if a story beat has no real counterpart, cut it. Label every character mention with its real function, and label story objects on the pages where they matter.

## Book structure

Cover, then the chapters (each with its own goal), then the full picture (the hero's last trip as a scene), then the cast cards (on the same page or the next), then the reference pages: What we don't know yet, a debugging index (symptom to page, using `data-goto` links), and a glossary (real term to story name).

Nothing before the full picture may show a cast list or a map of the whole system.
