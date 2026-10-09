# joelcrey.github.io

Personal website, built with Jekyll. Edit Markdown, push to `main`, and the GitHub Action in
`.github/workflows/pages.yml` rebuilds and publishes the site.

## Where things live

| To change…                | Edit                                     |
|---------------------------|------------------------------------------|
| CV                        | `cv.md` (and replace `acadcv.pdf`)       |
| Research intro            | `research.md`                            |
| A research project        | `_research/<any name>.md`                |
| About me                  | `aboutme.md`                             |
| Homepage banner           | `index.html`                             |
| Sidebar menu, contact     | `_includes/sidebar.html`, `_config.yml`  |
| Page frame (head, scripts)| `_layouts/default.html`                  |

## Writing a post

1. Copy `_drafts/example-math-post.md` into `_posts/` as `YYYY-MM-DD-short-title.md`.
2. Set `title`, `category` (`math` or `thoughts`) and optionally `summary` / `image`.
3. Push. It appears in the sidebar and on the homepage, at `/posts/short-title.html`.

Drafts in `_drafts/` are never published.

## Research projects

One file per project in `_research/`, with any file name (Obsidian-friendly):

```yaml
---
title: On the Watanabe–Yoshida conjecture
summary: One or two sentences for the card on the Research page.
order: 2              # position on the Research page and in the menu
slug: watanabe-yoshida   # optional: URL becomes /research/watanabe-yoshida.html
published: false      # optional: keep it hidden while unfinished
---
```

## Runnable Sage cells

Put `sagecell: true` in a page's front matter, and every ```` ```sage ```` code block becomes a cell
readers can run on [SageMathCell](https://sagecell.sagemath.org). Cells on a page share one session.
To make a module available, add `sage_preload: /path/to/module.py` to the front matter: the page gets a
**Load module.py** button before the first cell, which sends the file (served by this site, so it also
works in the local preview) to the Sage session.

## Post series

Add `series: <key>` and `series_part: <n>` to the posts, and describe the series (title, extra
files) in `_data/series.yml`. Each post then shows a box linking all the parts.

## Math and line breaks

Same as Obsidian: `$x$` is inline, `$$x$$` is displayed (even mid-line), `\$` is a
literal dollar sign. A single line break is kept as a line break.
(`_plugins/obsidian_math.rb` does the translation.)

## Preview locally

    bundle install                 # once
    bundle exec jekyll serve --drafts --unpublished --livereload

then open http://localhost:4000. `--drafts --unpublished` also shows unfinished posts and projects;
leave them out to see exactly what will be published.

## Credits

Design: [Editorial by HTML5 UP](https://html5up.net) (CCA 3.0, see `LICENSE.txt`).
Icons: Font Awesome.
