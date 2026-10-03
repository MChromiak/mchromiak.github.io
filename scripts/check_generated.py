#!/usr/bin/env python3
"""Validate generated links, SEO metadata, structured data, and assets."""

import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


HOST = "mchromiak.github.io"
REQUIRED = ("index.html", "robots.txt", "sitemap.xml", "favicon.ico")


class PageAudit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []
        self.links = []
        self.canonicals = []
        self.json_ld = []
        self._json_ld_parts = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        rel = set(attrs.get("rel", "").split())
        if tag == "link" and rel & {"stylesheet", "icon", "manifest", "preload"}:
            self.assets.append(attrs["href"])
        if tag == "link" and "canonical" in rel and attrs.get("href"):
            self.canonicals.append(attrs["href"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag in {"img", "script", "source", "video", "audio"}:
            if attrs.get("src"):
                self.assets.append(attrs["src"])
            if attrs.get("poster"):
                self.assets.append(attrs["poster"])
            if attrs.get("srcset"):
                self.assets.extend(part.strip().split()[0] for part in attrs["srcset"].split(","))
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._json_ld_parts = []

    def handle_data(self, data):
        if self._json_ld_parts is not None:
            self._json_ld_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._json_ld_parts is not None:
            self.json_ld.append("".join(self._json_ld_parts))
            self._json_ld_parts = None

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


def exists_in_output(root, target):
    if target is None or not target.is_relative_to(root):
        return False
    return target.is_file() or (target.is_dir() and (target / "index.html").is_file())


def schema_objects(value):
    if isinstance(value, list):
        return value
    if isinstance(value, dict) and isinstance(value.get("@graph"), list):
        return value["@graph"]
    return [value]


def normalized_url(url):
    parsed = urlsplit(url)
    path = parsed.path.rstrip("/") or "/"
    return f"{parsed.scheme}://{parsed.netloc}{path}"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
    errors = [f"missing required file: {name}" for name in REQUIRED if not (root / name).is_file()]
    pages = list(root.rglob("*.html"))
    audits = {}

    for page in pages:
        parser = PageAudit()
        parser.feed(page.read_text(encoding="utf-8"))
        audits[page.resolve()] = parser
        for url in parser.assets:
            try:
                target = local_path(root, page, url)
            except ValueError:
                errors.append(f"development asset URL in {page.relative_to(root)}: {url}")
                continue
            if target is not None and not target.is_file():
                errors.append(f"missing asset in {page.relative_to(root)}: {url}")

        for url in parser.links:
            try:
                target = local_path(root, page, url)
            except ValueError:
                errors.append(f"development link in {page.relative_to(root)}: {url}")
                continue
            if target is not None and not exists_in_output(root, target):
                errors.append(f"broken internal link in {page.relative_to(root)}: {url}")

        for raw in parser.json_ld:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"invalid JSON-LD in {page.relative_to(root)}: {exc.msg}")
                continue
            for item in schema_objects(data):
                if not isinstance(item, dict):
                    continue
                item_type = item.get("@type")
                if item_type == "BlogPosting":
                    required = {"headline", "description", "url", "datePublished", "dateModified", "image", "author"}
                    absent = sorted(required - item.keys())
                    if absent:
                        errors.append(f"incomplete BlogPosting in {page.relative_to(root)}: {', '.join(absent)}")
                    if parser.canonicals and normalized_url(item.get("url", "")) != normalized_url(parser.canonicals[0]):
                        errors.append(f"BlogPosting URL differs from canonical in {page.relative_to(root)}")
                if item_type == "BreadcrumbList":
                    items = item.get("itemListElement")
                    positions = [entry.get("position") for entry in items] if isinstance(items, list) else []
                    if not positions or positions != list(range(1, len(positions) + 1)):
                        errors.append(f"invalid BreadcrumbList in {page.relative_to(root)}")

    sitemap = ET.parse(root / "sitemap.xml")
    for node in sitemap.findall(".//{*}loc"):
        url = (node.text or "").strip()
        target = local_path(root, root / "index.html", url)
        if not exists_in_output(root, target):
            errors.append(f"sitemap URL has no generated page: {url}")
            continue
        page = target if target.is_file() else target / "index.html"
        parser = audits.get(page.resolve())
        if parser is None or len(parser.canonicals) != 1:
            errors.append(f"sitemap page must have one canonical: {url}")
        elif normalized_url(parser.canonicals[0]) != normalized_url(url):
            errors.append(f"sitemap URL differs from canonical: {url}")

    if errors:
        print("Generated-site validation failed:")
        print("\n".join(f"  {item}" for item in sorted(set(errors))[:30]))
        return 1
    print(f"Checked links, structured data, sitemap, and assets in {len(pages)} generated pages: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
