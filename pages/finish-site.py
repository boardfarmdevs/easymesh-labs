#!/usr/bin/env python3
"""Finish a built Pages site: the labs bar on every page, .nojekyll and build.json.

Kept once, in easymesh-labs (pages/); the labs' shared Pages workflow
(.github/workflows/labs-pages.yml) runs it in every repository with a site. Run it from
the root of the repository whose site was built:

    python3 <easymesh-labs>/pages/finish-site.py [SITE]          (default dist/site)

- adds <script src="https://mesh.vcpe.dev/labs-bar.js" data-project="<repo>" defer> to the
  head of every HTML page, except a page that says <meta name="labs-bar" content="off">
  (a full-screen tool). The bar is served once, from the umbrella's site, so a change to
  it is one change; this repository's site (easymesh-labs) carries the file itself;
- writes .nojekyll and build.json (repository, revision, the bar, pages with the bar);
- fails when the site has no index.html or a page has no head.

The repository name comes from GITHUB_REPOSITORY in Actions, else from the origin
remote of the current directory.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BAR = "labs-bar.js"
BAR_URL = "https://mesh.vcpe.dev/labs-bar.js"
HOME = "easymesh-labs"
OPT_OUT = re.compile(r"""<meta\s+name=["']labs-bar["']\s+content=["']off["']""", re.I)
HEAD_END = re.compile(r"</head\s*>", re.I)


def git(*args):
    return subprocess.run(
        ["git", "-C", str(Path.cwd()), *args], capture_output=True, text=True, check=False
    ).stdout.strip()


def repository():
    slug = os.environ.get("GITHUB_REPOSITORY") or re.sub(
        r"^.*github\.com[:/]|\.git$", "", git("remote", "get-url", "origin")
    )
    owner, _, name = slug.partition("/")
    if not owner or not name:
        raise SystemExit(f"cannot tell the repository ({slug!r})")
    return owner, name


def finish(site):
    if not (site / "index.html").is_file():
        raise SystemExit(f"{site}: no index.html; build the site first")
    owner, name = repository()
    if name == HOME:
        shutil.copyfile(HERE / BAR, site / BAR)  # the one copy the other sites load
    with_bar, without = [], []
    for page in sorted(site.rglob("*.html")):
        relative = page.relative_to(site).as_posix()
        html = page.read_text(encoding="utf-8")
        if OPT_OUT.search(html):
            without.append(relative)
            continue
        if f'data-project="{name}"' in html and BAR_URL in html:
            with_bar.append(relative)  # already finished
            continue
        if not HEAD_END.search(html):
            raise SystemExit(f"{relative}: no </head> to add the labs bar to")
        tag = f'<script src="{BAR_URL}" data-project="{name}" defer></script>\n'
        head = HEAD_END.search(html).start()
        page.write_text(html[:head] + tag + html[head:], encoding="utf-8")
        with_bar.append(relative)
    (site / ".nojekyll").touch()
    revision = os.environ.get("GITHUB_SHA") or git("rev-parse", "HEAD")
    build = {
        "repository": f"{owner}/{name}",
        "revision": revision,
        "labs_bar": BAR_URL,
        "pages_with_bar": with_bar,
        "pages_without_bar": without,
    }
    if name == HOME:
        build["labs_bar_sha256"] = hashlib.sha256((HERE / BAR).read_bytes()).hexdigest()
    (site / "build.json").write_text(json.dumps(build, indent=2) + "\n")
    print(
        f"{site}: labs bar ({BAR_URL}) on {len(with_bar)} pages, {len(without)} full-screen "
        f"pages without; {owner}/{name} @ {revision[:12]}"
    )


if __name__ == "__main__":
    finish(Path(sys.argv[1] if len(sys.argv) > 1 else Path.cwd() / "dist" / "site").resolve())
