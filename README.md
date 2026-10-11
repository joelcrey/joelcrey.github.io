# joelcrey.github.io

Personal website, built with Jekyll. Edit Markdown, push to `main`, and the GitHub Action in
`.github/workflows/pages.yml` rebuilds and publishes the site.

## Where things live

| To change…                | Edit                                     |
|---------------------------|------------------------------------------|
| CV (web page and PDF)     | `cv/cv.xlsx`, see below                  |
| Research intro            | `research.md`                            |
| A research project        | `_research/<any name>.md`                |
| About me                  | `aboutme.md`                             |
| Homepage banner           | `index.html`                             |
| Top menu                  | `_includes/header.html`                  |
| Contact details (footer)  | `_config.yml`, `_includes/footer.html`   |
| Extra styles              | `assets/css/custom.css`                  |
| Page frame (head, scripts)| `_layouts/default.html`                  |

## Updating the CV

Everything in the CV comes from `cv/cv.xlsx`:

- **Sections** sheet: the sections, in order. `type` is `list` (entries from the sheet with the same
  name), `events` (rows of the Events sheet with the given `contribution`) or `text` (the `text`
  column). `web`/`pdf` say where the section appears; `details_in_pdf: no` hides talk titles (or the
  `details` column) in the PDF; `web_collapsed: yes` makes the section collapsible (closed) on the web page.
- **Events** sheet: every conference, workshop, seminar or school, one row each. `contribution` is
  `invited talk`, `talk`, `poster` or `attended` (blank means attended), and `title` is the title of
  your talk or poster. The CV puts each event in Invited Talks, Other talks, Posters or Conferences
  and courses accordingly.
- Other sheets (Education, Publications, Visits, Organization): one row per entry.
- In every sheet, put older entries first, so new ones go at the bottom; the CV shows them newest
  first. `web`/`pdf` can hide a single row; blank means yes. Write `*italics*` or `**bold**` in any cell.
- **Places** sheet: the coordinates of each `place` for the map on the homepage. Every entry of
  Education, Visits, Organization and Events with a place listed here gets a pin; entries that have
  not ended yet show as upcoming. The build script names any place missing from this sheet.

When you push, GitHub regenerates the CV page and `acadcv.pdf`. To see the result locally first:

    python3 cv/build_cv.py --pdf      # needs LuaLaTeX; without --pdf only the web page is updated

Name, title and contact details are in `cv/acadcv.tex`, which also sets the style.

## Writing a post

1. Copy `_drafts/example-math-post.md` into `_posts/` as `YYYY-MM-DD-short-title.md`.
2. Set `title`, `category` (`math` or `thoughts`) and optionally `summary` / `image`.
3. Push. It appears on the Math thoughts page (`math.html`) and the homepage, at `/posts/short-title.html`.

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

## Collapsible sections

Add `collapsible: true` to the front matter of a post or research page and every section under
its top-level headings (`##`, or `###` if that is the largest used) opens and closes by clicking
its title; `collapsible: closed` starts them closed. The Markdown stays the same, so it still
reads normally in Obsidian.

## Preview locally

    bundle install                 # once
    bundle exec jekyll serve --drafts --unpublished --livereload

then open http://localhost:4000. `--drafts --unpublished` also shows unfinished posts and projects;
leave them out to see exactly what will be published.

## Credits

Design: [Editorial by HTML5 UP](https://html5up.net) (CCA 3.0, see `LICENSE.txt`).
Icons: Font Awesome.
