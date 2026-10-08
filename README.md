# joelcrey.github.io

Personal website, built by GitHub Pages with Jekyll. Edit Markdown, push, and the site rebuilds.

## Where things live

| To change…                | Edit                                     |
|---------------------------|------------------------------------------|
| CV                        | `cv.md` (and replace `acadcv.pdf`)       |
| Research summary          | `research.md`                            |
| About me                  | `aboutme.md`                             |
| Homepage banner           | `index.html`                             |
| Sidebar menu, contact     | `_includes/sidebar.html`, `_config.yml`  |
| Page frame (head, scripts)| `_layouts/default.html`                  |

## Writing a post

1. Copy `_drafts/example-math-post.md` into `_posts/` as `YYYY-MM-DD-short-title.md`.
2. Set `title`, `category` (`math` or `thoughts`) and optionally `summary` / `image`.
3. Push. It appears in the sidebar and on the homepage, at `/posts/short-title.html`.

Drafts in `_drafts/` are never published.

## Math

Write LaTeX between double dollars: `$$x^2$$` inside a sentence is inline;
`$$ ... $$` on its own paragraph is displayed. Don't use `\(...\)` or `$...$`,
Markdown eats the backslashes.

## Preview locally

    bundle install                 # once
    bundle exec jekyll serve --drafts

then open http://localhost:4000.

## Credits

Design: [Editorial by HTML5 UP](https://html5up.net) (CCA 3.0, see `LICENSE.txt`).
Icons: Font Awesome.
