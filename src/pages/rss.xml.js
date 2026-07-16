import rss from "@astrojs/rss";
import { getCollection } from "astro:content";

export async function GET(context) {
  const articles = (await getCollection("articles", ({ data }) => !data.draft)).sort(
    (a, b) => b.data.date.valueOf() - a.data.date.valueOf(),
  );
  return rss({
    title: "Pradeep Pandey: Articles",
    description: "Technical writing on mathematics, machine learning, and transformer internals.",
    site: context.site,
    items: articles.map((a) => ({
      title: a.data.title,
      description: a.data.description,
      pubDate: a.data.date,
      link: `/articles/${a.id}/`,
    })),
  });
}
