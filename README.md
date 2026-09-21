# Michał Chromiak's blog

Pelican source for [mchromiak.github.io](https://mchromiak.github.io/).
Work on the `pelican` branch; GitHub Actions publishes it automatically.

## Setup

```bash
conda env create -f environment.yml
conda activate pelican_env
```

For an existing environment:

```bash
conda env update -f environment.yml --prune
```

## Daily workflow

```bash
make dev PORT=8000   # live preview at http://127.0.0.1:8000
make check           # production build plus local-asset validation
git push origin pelican
```

A push to `pelican` builds and publishes the site with Pelican's official
GitHub Pages workflow. Run `make check` before pushing to catch missing local
assets.

Articles and their images live in `content/articles/`. Shared assets live in
`content/static_files/`, and theme customizations in `themes/pelican-bootstrap3/`.
Use `Status: draft` for unfinished articles; production builds exclude drafts.

Configuration is split conventionally:

- `pelicanconf.py`: local development and common site settings;
- `publishconf.py`: production URL, feeds, analytics, and comments;
- `requirements.txt`: pinned Python packages used locally and in CI.

Generated files stay in `output/` and are not committed.
