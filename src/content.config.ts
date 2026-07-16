import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// Files starting with "_" are ignored: use that for drafts/templates.
const articles = defineCollection({
  loader: glob({ pattern: "**/[^_]*.md", base: "./src/content/articles" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    // Set math: true to load KaTeX styles on that article only.
    math: z.boolean().default(false),
    draft: z.boolean().default(false),
  }),
});

export const collections = { articles };
