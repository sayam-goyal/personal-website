import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://sayamgoyal.com',
  output: 'static',
  trailingSlash: 'always',
  markdown: {
    shikiConfig: { theme: 'github-dark' },
  },
});
