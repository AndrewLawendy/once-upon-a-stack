# Contributing

Thanks for helping. Every change goes through a pull request, and the maintainer reviews and approves each one.

## Before you start

For anything bigger than a small fix, please open an issue first, so nobody spends time on something that won't fit.

## Making a change

1. Fork the repo and make a branch.
2. Make your change. The skill lives in `skills/once-upon-a-stack/`.
3. Build a small book with it, and run the check:

   ```
   python3 skills/once-upon-a-stack/scripts/build.py "<library>/<slug>--<topic>"
   node skills/once-upon-a-stack/scripts/check.mjs "<library>/<slug>--<topic>"
   ```

4. Look at the screenshots in the book's `.source/check/` folder. The check can't judge the art.
5. Open a pull request and fill in the template.

New commits on a pull request clear any earlier approval, so it gets reviewed again. Pull requests are squashed when merged.

## What makes a good change

- **Stories:** each chapter opens on what the hero wants, and each character arrives because something broke. See `references/story.md`.
- **Facts:** claims come from primary sources and are labelled Verified, Inferred or Unknown. See `references/research.md`.
- **Motion:** slow and small. It should never compete with the page.
- **Art styles:** a new style needs its own folder in `assets/styles/`, with fonts that may be redistributed.
- **Simple:** no new dependencies without a good reason.

## Please don't include

Secrets, tokens or personal data, in code or in a book.
