#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Commit or remove local changes before deploying." >&2
  exit 1
fi

git fetch origin \
  refs/heads/pelican:refs/remotes/origin/pelican \
  refs/heads/main:refs/remotes/origin/main

if [[ "$(git rev-parse HEAD)" != "$(git rev-parse refs/remotes/origin/pelican)" ]]; then
  echo "Push this source commit to origin/pelican before deploying." >&2
  exit 1
fi

make check

deploy_branch="codex/pages-publish-$(date -u +%Y%m%dT%H%M%SZ)-$$"
git branch "$deploy_branch" refs/remotes/origin/main
ghp-import -n -m "Publish Pelican site from $(git rev-parse --short HEAD)" \
  -b "$deploy_branch" output

if ! git push origin "$deploy_branch:main"; then
  echo "Publish failed; generated commit remains on $deploy_branch." >&2
  exit 1
fi

git fetch origin refs/heads/main:refs/remotes/origin/main
if git merge-base --is-ancestor "$deploy_branch" refs/remotes/origin/main; then
  git branch -D "$deploy_branch"
else
  echo "Published branch could not be verified; retained $deploy_branch." >&2
  exit 1
fi
