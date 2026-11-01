# Research

Depth comes from specific questions followed through primary sources, not from reviewing sections. A broad pass is only good for the map.

## Three passes

1. **Map.** Who exists, who talks to whom, and which problem forced each part to exist. Use this to draft the chain and to find what's missing.
2. **Journeys.** Follow one thing end to end: a call, a login, a render, a bill. Split chapters by journey, not by repo or module, and cross every boundary the journey crosses.
3. **"Wait, how?"** Ask these of every step:
   - Who creates this, and from what?
   - Why does it exist? What breaks without it?
   - What if it arrives late, twice, out of order, or never?
   - Who else reads or depends on it?
   - What does a person actually see when it goes wrong?
   - What does this fix cost, and what new problem does it create?
   - What simpler thing would someone try first, and exactly why does it fail?

Each answer usually raises new questions. A step is finished when each question has a source or is logged as unknown. Unknowns are a normal result. Guessing is not.

## Sources

| Topic type | Start with | Then | Cite as |
|---|---|---|---|
| Your own code | Code on the branch that matches the question | Tests, ADRs and contracts in the repo, then tickets, chat and internal docs | repo, file, function, commit |
| Open source (React, Kubernetes, Grafana) | Source code at a pinned release tag, design docs, RFCs and KEPs | Official docs | repo, file, tag or doc URL with version |
| Concepts | Specs, original papers | Reputable articles | title, link, date |

- **Pin versions.** Get real commit hashes and tags. They go on the cover stamp.
- **Docs and KBs describe. Code decides.** Use a KB to find where to look, then confirm in the source.
- **Tests and comments often hold the "why".** Look there and in ADRs and commit history before inferring a reason.
- **Deployed isn't the same as latest.** When a chapter describes a specific environment, say which version the facts came from.
- **Never put secrets, tokens or customer personal data in a book.**

## Evidence labels

- **Verified:** read directly in a primary source, with the citation.
- **Inferred:** a reasoned conclusion. Say what it rests on. Most "why" answers start here, so look for ADRs, tickets or history that would upgrade them.
- **Unknown:** couldn't be determined. Say what would settle it and who could answer.

Scenes also say where they come from:
- **This really happened:** a real incident or bug, with the ticket or date.
- **Imagine if:** what the logic implies, with no record of it actually happening.

## Subagent brief

Dispatch one subagent per journey. Give it this contract and its journey, and have it write `.source/facts/NN-<journey>.md`:

```
Journey: <what to follow, from where to where>
Sources: <repos at pinned refs, doc URLs>
Read only. Don't run anything that changes state.

Write a dossier with these parts, in order:
1. Path: each step in order, with the component and source citation.
2. Details: for each step, answers to who creates it, why it exists,
   what breaks without it, late/twice/out of order/never, who else
   depends on it, what a person sees when it fails, and what it costs.
3. Why it had to be this way: the simpler approaches, why each fails, and what the next fix misses. These become chain links.
4. Real incidents: tickets, dates and links, or "none found".
5. Names: exact field names, messages, config keys and defaults.
6. Unknowns: what you couldn't determine, what would settle it, who could answer.

Label every claim Verified, Inferred or Unknown. Verified claims need a
file and function or a URL. No story language.
```

## Fact-check brief

Give a fresh subagent, one that didn't research or write the book, this contract. It reads the built pages in `.source/pages/`, the dossiers in `.source/facts/`, and the cited sources themselves, and writes `.source/facts/fact-check.md`.

```
Book: <library>/<book>/.source/pages/ (story text, scene labels and For grown-ups notes)
Dossiers: <library>/<book>/.source/facts/
Read only. Don't edit the pages.

For every factual claim on every page, including numbers, dates, names, quotes,
defaults and "what people see" lines:
1. Find its source: the citation on the page, or the dossier.
2. Open the source itself, not the dossier's summary of it.
3. Give one verdict:
   - Correct
   - Overstated: the page says more than the source (wider, stronger, "only", "always")
   - Wrong: the source says otherwise
   - Mislabelled: marked Verified but only Inferred, or the reverse
   - Unsupported: no source found
   - Misquoted: quotation marks around words the source doesn't use

Also flag any character named by description without its label ("the runner"
for a labelled character), and any story beat with no real counterpart.

Report only the claims that aren't Correct, with page, the exact text, the
source and its exact words, and the fix. End with the count checked per page.
```

Story simplifications are fine when the notes give the exact version. A claim the story makes stronger than its notes is Overstated.
