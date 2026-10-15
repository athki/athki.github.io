# christianpfrang.com

Static site, served by GitHub Pages from this repo (custom domain via `CNAME`).

## Where things live

| File | What it is |
|---|---|
| `content.yml` | **Every piece of text on the site** except the artifact entries. Edit this to change copy. |
| `artifacts.yml` | **The Artifacts page entries**, newest first. To add one, paste a new block at the top (template in the file's header). |
| `templates/` | The layout (Jinja templates): `base.html` (nav + footer), `index.html`, `artifacts.html`, `impressum.html`, `datenschutz.html`. |
| `site.css` | The look. Colours are variables at the top. |
| `build.py` | Turns `content.yml` + `artifacts.yml` + `templates/` into the HTML pages below. |
| `index.html`, `artifacts.html`, `impressum.html`, `datenschutz.html` | **Generated.** Don't edit by hand; edit `content.yml` and rebuild. |
| `images/og.png`, `images/favicon.svg` | Link-preview image and tab icon. |
| `CNAME` | Tells GitHub Pages to serve the site at www.christianpfrang.com. Don't delete. |
| `files/` | PDFs linked from the Artifacts page. |

## Change a text and preview it

```bash
pip install pyyaml jinja2      # once
python3 build.py               # regenerates the four HTML pages
python3 -m http.server 8000    # open http://localhost:8000
```

Then commit and push; GitHub Pages picks it up in about a minute. Commit the generated HTML too — Pages serves the files as they are, there is no build step on GitHub's side.

The cheapest way to iterate: open the repo in Claude Code and say "change the belief line on the trust card to …"; it edits `content.yml`, runs the build, and you look at the result.

## Before going live

Search `content.yml` for `TODO`:

- `where.entries`: the event dates (or delete an entry). Each entry can also take a `link` to the event page.
- `legal`: street, postcode/city and USt-IdNr. The Impressum and Datenschutzerklärung are drafts written for this exact setup (static page, no cookies, no analytics, no forms, GitHub Pages as host). Read them once; they are not legal advice.

## Notes

- `images/profile.jpg` is the photo from the previous site, kept in case it comes back; nothing links to it right now.
- `.nojekyll` tells GitHub Pages to serve the files as-is instead of running Jekyll over them.
- Fonts are the system font stack, so nothing is loaded from Google or any other third party.
