// @ts-check
import { defineConfig } from "astro/config";
import { unified } from "@astrojs/markdown-remark";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
export default defineConfig({
  site: "https://pradeeppandey.name.np",
  // Fetch pages on link hover so SPA navigations feel instant.
  prefetch: { prefetchAll: true },
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
    shikiConfig: {
      // Dual-theme code blocks: colors switch with the site theme via CSS vars.
      themes: { light: "github-light", dark: "github-dark" },
      defaultColor: false,
    },
  },
});
