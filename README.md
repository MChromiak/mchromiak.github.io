# Michał Chromiak's blog

This is the Pelican source for [mchromiak.github.io](https://mchromiak.github.io/).
The `pelican` branch contains articles, theme customizations, and build tools.
GitHub Pages serves the generated site from the root of `main`. Do not edit
`main` by hand.

## Set up

From this repository's root directory:

```bash
conda env create -f environment.yml
conda activate pelican_env
```

If `pelican_env` already exists, update it with
`conda env update -f environment.yml --prune`. The pinned Python packages live
in `requirements.txt`; `environment.yml` includes that file so local builds and
GitHub Actions use the same versions.

## Write and preview

Put articles and their media under `content/articles/`; shared images, CSS, and
JavaScript live under `content/static_files/`. The customized, vendored theme
is `custom/pelican-bootstrap3/`. Use `Status: draft` for unfinished articles.

```bash
make dev PORT=8000
```

Open `http://127.0.0.1:8000/`. The `dev` target uses Pelican's auto-reload and
HTTP server. It writes to ignored `output-preview/`, leaving the production
build alone. Run `make preview` for a one-shot local build.

## Validate and publish

```bash
make check
```

This builds with `publishconf.py` into ignored `output/` and checks generated
pages for missing site-local links and assets. GitHub Actions runs the same
check on pushes and pull requests to `pelican`.

After reviewing the build, commit and push the source to `pelican`, then run:

```bash
make deploy
```

Deployment requires a clean working tree and requires the current commit to
match `origin/pelican`. It fetches the latest `main`, generates a new Pages
commit based on it, and uses a normal fast-forward push. A concurrent update
causes the push to fail rather than overwrite it. The generated commit includes
`.nojekyll`, so GitHub Pages serves Pelican's HTML without a Jekyll rebuild.
Wait for the `pages-build-deployment` workflow to finish before checking the
live site.

The publishing domain, feeds, analytics, and comments are configured in
`publishconf.py`; local settings and site structure live in `pelicanconf.py`.

## Branches

| Branch | Purpose |
| --- | --- |
| `pelican` | Source and pull requests; this is the branch to clone and edit. |
| `main` | Generated GitHub Pages output; updated only by `make deploy`. |

This branch-based setup follows the [Pelican publishing guidance](https://docs.getpelican.com/en/stable/tips.html)
and [GitHub Pages branch-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
