# CYNTP Website — Claude Instructions

## Deployment Workflow

NEVER run `wrangler deploy` directly. The site auto-deploys from GitHub on push to main. The correct workflow for any change to the live site is:

1. Make the edits
2. `git add` the changed files
3. `git commit` with a clear message describing what changed
4. `git push origin main`
5. Let the GitHub-to-Cloudflare auto-deploy handle the rest

Running `wrangler deploy` without committing first causes the live site to drift out of sync with the GitHub repo. The next GitHub-triggered deploy will then overwrite the wrangler-deployed changes, making edits appear to "disappear" from the live site.

If a user explicitly asks to deploy without committing, push back and explain why. Only bypass this rule if the user confirms after that pushback.

Also: at the end of every session where edits were made, always commit and push before stopping. Never leave uncommitted changes sitting locally.
