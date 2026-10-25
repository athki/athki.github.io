#!/usr/bin/env python3
"""Build christianpfrang.com from content.yml + artifacts.yml + templates/.

    python3 build.py           # writes index.html, artifacts.html, impressum.html, datenschutz.html
    python3 -m http.server     # then open http://localhost:8000 to preview

Needs: pip install pyyaml jinja2
"""
import datetime
import hashlib
import pathlib
import re
import sys

try:
    import jinja2
    import markupsafe
    import yaml
except ImportError:
    sys.exit("Missing packages. Run:  pip install pyyaml jinja2")

ROOT = pathlib.Path(__file__).resolve().parent

LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def paragraphs(text: str) -> markupsafe.Markup:
    """Blank line in content.yml -> new <p>; [text](https://...) -> link. Everything else is escaped."""
    out = []
    # A folded (>-) YAML block turns each blank line into a single "\n".
    sep = r"\n\s*\n" if re.search(r"\n\s*\n", text) else r"\n"
    for para in re.split(sep, text.strip()):
        html = str(markupsafe.escape(" ".join(para.split())))
        html = LINK.sub(r'<a href="\2" rel="noopener">\1</a>', html)
        out.append(f'<p class="lead">{html}</p>')
    return markupsafe.Markup("\n    ".join(out))

# output file -> template file
PAGES = {
    "index.html": "index.html",
    "artifacts.html": "artifacts.html",
    "impressum.html": "impressum.html",
    "datenschutz.html": "datenschutz.html",
}


def main() -> None:
    content = yaml.safe_load((ROOT / "content.yml").read_text(encoding="utf-8"))
    content["artifacts"] = yaml.safe_load((ROOT / "artifacts.yml").read_text(encoding="utf-8")) or []
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(ROOT / "templates"),
        autoescape=jinja2.select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=jinja2.StrictUndefined,  # a typo in content.yml fails loudly instead of rendering blank
    )
    env.filters["paragraphs"] = paragraphs
    built = datetime.date.today().isoformat()
    # Changes whenever site.css changes, so browsers never show a stale stylesheet.
    css_version = hashlib.sha256((ROOT / "site.css").read_bytes()).hexdigest()[:8]
    for out_name, tpl_name in PAGES.items():
        html = env.get_template(tpl_name).render(**content, built=built, css_version=css_version)
        (ROOT / out_name).write_text(html, encoding="utf-8")
        print(f"wrote {out_name}")


if __name__ == "__main__":
    main()
