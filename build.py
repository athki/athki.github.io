#!/usr/bin/env python3
"""Build christianpfrang.com from content.yml + artifacts.yml + templates/.

    python3 build.py           # writes index.html, artifacts.html, impressum.html, datenschutz.html
    python3 -m http.server     # then open http://localhost:8000 to preview

Needs: pip install pyyaml jinja2
"""
import datetime
import hashlib
import pathlib
import sys

try:
    import jinja2
    import yaml
except ImportError:
    sys.exit("Missing packages. Run:  pip install pyyaml jinja2")

ROOT = pathlib.Path(__file__).resolve().parent

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
    built = datetime.date.today().isoformat()
    # Changes whenever site.css changes, so browsers never show a stale stylesheet.
    css_version = hashlib.sha256((ROOT / "site.css").read_bytes()).hexdigest()[:8]
    for out_name, tpl_name in PAGES.items():
        html = env.get_template(tpl_name).render(**content, built=built, css_version=css_version)
        (ROOT / out_name).write_text(html, encoding="utf-8")
        print(f"wrote {out_name}")


if __name__ == "__main__":
    main()
