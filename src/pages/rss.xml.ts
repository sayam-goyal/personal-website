import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getPosts } from '../lib/posts';
import { site } from '../config';
export async function GET(context: APIContext) {
  return rss({ title: `${site.name} — Field notes`, description: site.description, site: context.site!,
    items: (await getPosts()).map(post => ({ title: post.data.title, pubDate: post.data.date, description: post.data.description, link: `/blog/${post.id}/` })) });
}
