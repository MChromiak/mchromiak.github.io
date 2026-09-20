#!/usr/bin/env python3
"""Check that generated pages and their site-local references exist."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


SITE_HOST = "mchromiak.github.io"
REQUIRED = (
    "index.html",
    "robots.txt",
    "sitemap.xml",
    "favicon.ico",
    "static_files/img/favicon.svg",
    "static_files/site.webmanifest",
)


class ReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag in {"a", "link"} and attributes.get("href"):
            self.references.append(attributes["href"])
        if tag in {"img", "script", "iframe", "video", "audio", "source"}:
            if attributes.get("src"):
                self.references.append(attributes["src"])
            if attributes.get("srcset"):
                self.references.extend(
                    item.strip().split()[0]
                    for item in attributes["srcset"].split(",")
                    if item.strip()
                )
        if tag == "video" and attributes.get("poster"):
            self.references.append(attributes["poster"])
        if tag == "meta" and attributes.get("property") == "og:image":
            self.references.append(attributes.get("content", ""))

    handle_startendtag = handle_starttag


def resolve_reference(root, page, reference):
    parsed = urlsplit(reference)
    if parsed.hostname in {"localhost", "127.0.0.1"}:
        raise ValueError(f"development URL in production output: {reference}")
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return None
    if parsed.netloc and parsed.netloc.lower() != SITE_HOST:
        return None
    if not parsed.path and parsed.fragment:
        return None
    if not parsed.path and not parsed.netloc:
        return None

    path = unquote(parsed.path or "/")
    destination = root / path.lstrip("/") if path.startswith("/") else page.parent / path
    if not path or path.endswith("/") or destination.is_dir():
        destination /= "index.html"
    destination = destination.resolve()
    if not destination.is_relative_to(root):
        raise ValueError(f"reference escapes the output directory: {reference}")
    return destination


def check(root):
    root = root.resolve()
    problems = set()
    for name in REQUIRED:
        if not (root / name).is_file():
            problems.add(f"missing required file: {name}")

    pages = list(root.rglob("*.html"))
    checked = 0
    for page in pages:
        parser = ReferenceParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for reference in parser.references:
            if not reference:
                continue
            checked += 1
            try:
                destination = resolve_reference(root, page, reference)
            except ValueError as error:
                problems.add(f"{page.relative_to(root)}: {error}")
                continue
            if destination is not None and not destination.is_file():
                problems.add(f"{page.relative_to(root)}: {reference}")

    if problems:
        print(f"Found {len(problems)} missing or invalid site-local references:")
        for problem in sorted(problems)[:30]:
            print(f"  {problem}")
        if len(problems) > 30:
            print(f"  ... and {len(problems) - 30} more")
        return 1
    print(f"Checked {len(pages)} HTML pages and {checked} references: OK")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Pelican output directory")
    args = parser.parse_args()
    if not args.output.is_dir():
        parser.error(f"not a directory: {args.output}")
    return check(args.output)


if __name__ == "__main__":
    raise SystemExit(main())
