# Sayam Goyal — personal website

A lightweight, static Astro site with plain CSS, TypeScript, and a Markdown blog. No React, database, analytics, or external fonts. A small script handles the theme toggle; dark mode is the default, with a beige light mode and a saved preference. Host the generated files on Hostinger or any static web server.

## Develop

Use Node.js 24 (see `.nvmrc`).

```sh
npm ci
npm run dev
```

`npm run build` checks types and generates `dist/`. `npm run preview` serves that build locally. GitHub Actions runs the same build on pushes to `main` and pull requests.

## Make it yours

- Edit `src/config.ts` for your email, résumé, LinkedIn, Twitter, booking link, interests, and projects. Empty contact URLs show as coming soon rather than broken links. Project ideas are explicitly labeled as sample ideas.
- Add your résumé to `public/resume.pdf`, then set `resume: '/resume.pdf'`.
- Edit the introduction in `src/pages/index.astro` and colors/type in `src/styles/global.css`.
- The canonical domain is configured in `astro.config.mjs`.
- Remove or replace the clearly labeled sample article before launch.

## Write a post

Create `src/content/blog/my-post.md`:

```md
---
title: "My post"
description: "A short summary."
date: 2026-10-24
tags: ["ai"]
draft: false
---
Your writing goes here.
```

Commit and push the file. The build creates `/blog/my-post/`, updates the homepage and blog index, and adds it to `/rss.xml`. Posts are sorted newest first. `draft: true` excludes a post from all published routes and RSS, but the file is still visible in a public GitHub repo. Dates do not schedule publication: use `draft` until ready.

Use `.md` for now. MDX is deliberately not installed; add `@astrojs/mdx` and its integration if you later want components inside posts.

### Images and files

Keep a post at `src/content/blog/my-post/index.md` and its images beside it. Embed an image using `![Descriptive alt text](./chart.png)`. Astro processes local Markdown images during the build. General images can live in `src/assets/`. Files in `public/` are copied unchanged: `public/resume.pdf` is served at `/resume.pdf`. Commit normal images to Git; use external storage for large videos or datasets.

## Deploy to Hostinger

The output is static. Do not upload raw source files or `node_modules` to `public_html`.

**Manual:** run `npm run build`, then upload the **contents** of `dist/` to the domain’s `public_html` folder. The included `.htaccess` sets the directory index and custom 404; preserve or reconcile existing server configuration instead of overwriting it blindly.

**Automatic:** `.github/workflows/deploy.yml` builds and uploads via SFTP when repository variable `HOSTINGER_DEPLOY_ENABLED` is `true`.

Repository secrets:
- `HOSTINGER_SSH_HOST`: `92.113.28.123`
- `HOSTINGER_SSH_PORT`: `65002`
- `HOSTINGER_SSH_USER`: `u509134529`
- `HOSTINGER_SSH_PRIVATE_KEY`: dedicated private deployment key, stored only in GitHub Secrets

Authorize the corresponding public key under Hostinger SSH Access → Add SSH key. The local dedicated key is `~/.ssh/sayamgoyal_hostinger_deploy`; never commit it or print its private contents.

Set repository variable `HOSTINGER_SSH_DIRECTORY` to the confirmed absolute website directory, normally `/home/u509134529/domains/sayamgoyal.com/public_html`. Confirm it after connecting, rather than relying on the FTP-relative path. Deployment refuses non-public_html destinations. Back up an existing website before replacement; reconcile old PHP entrypoints and routing rules manually.

The verified ED25519 server public key is pinned in `.github/hostinger_known_hosts`, fingerprint `SHA256:s48iBU2xDmURYkPlWQlMOIoiaN+zSws6BJtMwRjWhzI`, checked against Hostinger's SSH Access page. Never replace it automatically on a mismatch. The workflow uses strict verification, key authentication, connection/transfer timeouts, and never prints the private key. It uploads assets before HTML, preserves `.htaccess`, and does not delete old files. Obsolete published pages must be removed manually. This upload is not atomic.

Once key authorization and destination are verified, enable deployment and use Actions → Deploy to Hostinger → Run workflow. Every subsequent push to main also deploys. Legacy `HOSTINGER_FTP_*` secrets and variables are no longer used.

## Project subdomains

Keep this site at `sayamgoyal.com`; deploy each application independently. Create a DNS record for e.g. `project.sayamgoyal.com` in Hostinger and add the domain to the application’s hosting configuration. Changes to a project do not require DNS updates after the initial setup.
