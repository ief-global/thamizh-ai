// @ts-check
import { defineConfig } from 'astro/config';

// Static output on purpose. The site is a phase (see WEBSITE-PLAN.md §2 in the design repo):
// it documents how the tool was designed, and it is archived when the app takes this domain.
export default defineConfig({
  site: 'https://thamizh-ai.org',
  trailingSlash: 'never',
  build: { format: 'file' },
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ta'],
    routing: { prefixDefaultLocale: false },
  },
});
