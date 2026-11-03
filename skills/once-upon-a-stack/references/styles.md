# Art styles

Pick one of these styles for each book and set `"style"` in `book.json`. Each style folder in `assets/styles/<id>/` holds its colors, fonts, panels, filters and an `example.svg` of one scene. Read that example before drawing, and draw every character and scene the same way.

| Style | `style` | Suits |
|---|---|---|
| Cut paper | `cut-paper` | Warm worlds, nature, animals |
| Woodcut | `woodcut` | Old crafts, history, security, anything with weight |
| Mid-century | `mid-century` | Playful systems, cities, machines |
| Stained glass | `stained-glass` | Hierarchies, big structures, grand subjects |
| Blueprint | `blueprint` | Engineering, infrastructure, how a machine fits together |
| Vintage poster | `vintage-poster` | Travel, networks, journeys, one bold idea |
| Pixel art | `pixel-art` | Software internals, games, retro computing |

## Choosing

Match the topic and mood first. Then look at the `style` of each book on the shelf (`<library>/*/.source/book.json`) and prefer one not used yet. Propose it in the table of contents in one line. If the user names a style, use that one. Don't invent a style unless the user asks for one.

## Drawing rules

**Cut paper:** flat, saturated shapes in layers. Apply `filter="url(#cut)"` to each layer for hand-cut edges and a soft shadow.

**Woodcut:** black ink on paper plus one spot color. Solid silhouettes with carved lines in the paper color: feathers, bark, ripples. Wrap the art in `filter="url(#grain)"` and keep figures on clear paper, with no rays or texture behind them.

**Mid-century:** simple geometry (circles, arches, triangles) with a thin black line drawn a few units off from the color. Patterns are zigzags and starbursts. Use flat teal, mustard, coral, black and cream.

**Stained glass:** everything is polygons with a dark lead stroke of 4-5 units. Break the background into random triangles of related colors, and split figures into a few facets with a lighter and a darker side.

**Blueprint:** lines only, no fills, on the blue grid. Draw the main shapes with a stroke of at least 3 and details with at least 2. Add dimension lines, callouts and short capital labels that say something true about the subject, at a font size of at least 15. One accent color marks the path of the story.

**Vintage poster:** big flat shapes with no outlines. Split a figure into a light and a dark half, and use stepped color bands for the sky and rays from the sun. A short slogan may sit in the scene using `font-family:var(--font-display)`.

**Pixel art:** draw on an 8-unit grid and only with `<rect>`s, from a small fixed palette. Generate scenes from sprite strings in a script so they stay on the grid. Limit pages' text, since the display font is wide and the body font is small.

## Every style

- Scene colors that should change with the theme use the classes `.sky`, `.sun`, `.hb`, `.hm`, `.hf`, `.tree`, `.path`, `.stump`, `.stump-top`. Art may also keep fixed colors, when it reads well on both themes.
- `{{tag|...}}` name tags already take the style's look.
- Check both themes in the screenshots. The check script flags hard-to-read text.
- Controls, page layout and motion rules don't change with the style.
