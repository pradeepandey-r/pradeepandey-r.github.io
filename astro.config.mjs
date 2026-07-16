// @ts-check
import { defineConfig } from "astro/config";
import { unified } from "@astrojs/markdown-remark";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import { fileURLToPath } from "node:url";

export default defineConfig({
  site: "https://pradeeppandey.name.np",
  // Fetch pages on link hover so SPA navigations feel instant.
  prefetch: { prefetchAll: true },
  vite: {
    define: {
      // Absolute path of this folder, injected as a compile-time constant.
      // Lets pages fs-check public/ files per request (CV, photo) regardless
      // of cwd (npm --prefix runs from the parent repo) or bundling.
      __SITE_ROOT__: JSON.stringify(fileURLToPath(new URL(".", import.meta.url))),
    },
  },
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
