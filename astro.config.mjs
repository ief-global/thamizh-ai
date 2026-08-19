// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Static output on purpose. The site is a phase (see WEBSITE-PLAN.md §2 in the design repo):
// it documents how the tool was designed, and it is archived when the app takes this domain.
export default defineConfig({
  site: 'https://thamizh-ai.org',
  trailingSlash: 'never',
  build: { format: 'file' },
  // The workers.dev URL and every preview build serve the same pages. Canonical tags in
  // Base.astro and this sitemap both point at the apex, so search engines treat
  // thamizh-ai.org as the real one. Letters cite that address; it should be the one that ranks.
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/render-check') && !page.includes('/ta'),
    }),
  ],
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ta'],
    routing: { prefixDefaultLocale: false },
  },
});
