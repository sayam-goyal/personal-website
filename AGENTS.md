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

**Automatic:** `.github/workflows/deploy.yml` is provided but remains disabled until you configure it. Each push to `main` will then build and upload through FTPS.

1. Back up the existing website, if any.
2. Add repository Actions secrets `HOSTINGER_FTP_HOST` (hostname only, preferably the certificate-matching hostname from Hostinger), `HOSTINGER_FTP_USER`, and `HOSTINGER_FTP_PASSWORD`.
3. Set Actions variable `HOSTINGER_FTP_DIRECTORY` to the remote directory visible to that FTP account. It defaults to `public_html`; some accounts are already rooted there and should use `.`. Verify your account’s path first.
4. Optionally configure protection rules on the GitHub `production` environment.
5. Set repository Actions variable `HOSTINGER_DEPLOY_ENABLED` to `true` and push to `main` or run the workflow manually.

Credentials stay in GitHub secrets. The transfer requires verified TLS and never prints the password. Automatic upload deliberately excludes `.htaccess` and does **not delete** remote files, so it preserves unrelated files and project directories. Consequently, when removing or renaming a published post, manually remove its obsolete remote folder. Upload/reconcile `.htaccess` manually if needed. This basic upload is not atomic; use release-directory switching if you later need atomic deployments.

## Project subdomains

Keep this site at `sayamgoyal.com`; deploy each application independently. Create a DNS record for e.g. `project.sayamgoyal.com` in Hostinger and add the domain to the application’s hosting configuration. Changes to a project do not require DNS updates after the initial setup.
