#!/usr/bin/env python3
"""Fail when a production page references a missing local asset."""

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


HOST = "mchromiak.github.io"
REQUIRED = ("index.html", "robots.txt", "sitemap.xml", "favicon.ico")


class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        rel = set(attrs.get("rel", "").split())
        if tag == "link" and rel & {"stylesheet", "icon", "manifest", "preload"}:
            self.urls.append(attrs["href"])
        if tag in {"img", "script", "source", "video", "audio"}:
            if attrs.get("src"):
                self.urls.append(attrs["src"])
            if attrs.get("poster"):
                self.urls.append(attrs["poster"])
            if attrs.get("srcset"):
                self.urls.extend(part.strip().split()[0] for part in attrs["srcset"].split(","))

    handle_startendtag = handle_starttag


def local_path(root, page, url):
    parsed = urlsplit(url)
    if parsed.hostname in {"localhost", "127.0.0.1"}:
        raise ValueError("development URL")
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return None
    if parsed.netloc and parsed.hostname != HOST:
        return None
    if not parsed.path:
        return None

    path = unquote(parsed.path)
    result = root / path.lstrip("/") if path.startswith("/") else page.parent / path
    if path.endswith("/"):
        result /= "index.html"
    return result.resolve()


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
    missing = [name for name in REQUIRED if not (root / name).is_file()]
    pages = list(root.rglob("*.html"))

    for page in pages:
        parser = Assets()
        parser.feed(page.read_text(encoding="utf-8"))
        for url in parser.urls:
            try:
                target = local_path(root, page, url)
            except ValueError:
                missing.append(f"{page.relative_to(root)}: {url}")
                continue
            if target is not None and not target.is_file():
                missing.append(f"{page.relative_to(root)}: {url}")

    if missing:
        print("Missing or invalid generated assets:")
        print("\n".join(f"  {item}" for item in sorted(set(missing))[:30]))
        return 1
    print(f"Checked assets in {len(pages)} generated pages: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
