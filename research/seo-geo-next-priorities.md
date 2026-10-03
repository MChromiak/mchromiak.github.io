# SEO and generative-search follow-up audit

Date: 2026-10-02

Scope: public `https://mchromiak.github.io` deployment and the Pelican source. This is a research note only; it does not change the production configuration or content.

## Executive conclusion

The technical baseline is now sound: the home page, `robots.txt`, `sitemap.xml`, the restored XLNet tag URL, and a current article all return HTTP 200; the sitemap and robots file are public; article pages have canonical URLs and `BlogPosting` markup; the About page has `ProfilePage`/`Person` markup; and a local crawl of the generated site found no broken internal links. Search results already surface recent articles including Typed Decision Models and Dragon Hatchling.

The next gains should come from measurement-led content work, richer article presentation, and faster discovery outside Google. There is no evidence-backed need for a separate "GEO layer" or an `llms.txt` file. Google states that its usual SEO requirements apply to AI Overviews and AI Mode, and explicitly says that special AI files, markup, or schema are unnecessary.

## Recommended priorities

### P0: use Search Console data to choose the next article work

1. Once a month and after material deployments, export the Search Console **Pages** and **Queries** views for the previous 28 and 90 days.
2. Prioritize pages with:
   - impressions but low CTR: improve the visible title and one-sentence summary/meta description;
   - average positions roughly 5-20: add missing explanations, primary-source evidence, and contextual internal links;
   - falling impressions: first separate site-specific decline from changing query demand;
   - "Crawled/Discovered - currently not indexed": inspect the page rather than repeatedly requesting indexing.
3. Compare Search Console clicks with GA4 sessions and engagement, accepting that the totals will not match exactly because the products measure different events.
4. Track ChatGPT referrals in GA4 using `utm_source=chatgpt.com`; OpenAI says ChatGPT Search adds this parameter to referral URLs.

Why first: without query and page data, further global changes are guesses. Google recommends Search Console for page/query performance, indexing, and Core Web Vitals, and suggests checking it about monthly or after content changes.

Sources: [Google: Get started with Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start), [Google: combine Search Console and Analytics](https://developers.google.com/search/docs/monitor-debug/google-analytics-search-console), [OpenAI: Publishers and Developers FAQ](https://help.openai.com/en/articles/12627856).

### P1: improve the pages that already have demand

For the pages selected from Search Console, make the value genuinely distinctive:

- add an explicit answer or thesis near the opening, then develop it;
- cite the original paper, official implementation, dataset, and benchmark protocol close to the claims they support;
- include original analysis: a derivation, reproduced result, worked example, comparison with controlled assumptions, or a clearly labeled conceptual diagram;
- state what the evidence establishes and what it does not, without repetitive defensive caveats;
- update an article only when the body changed materially and keep the visible and structured `dateModified` aligned;
- link to two or three relevant articles in explanatory sentences with descriptive anchor text, not only through generic related-post widgets.

This is the most defensible "GEO" work. Google's current generative-search guidance prioritizes unique, expert-led, non-commodity content and normal SEO fundamentals. Google also recommends clear authorship, first-hand expertise, useful source links, and contextual internal links.

The clearest existing candidates are the oldest articles whose opening copy and summaries are still weaker than the recently revised paper explainers, especially **The power of patterns - embrace the hurricanes**, **Neural Networks Primer**, and the older Transformer introduction. Search Console should decide their order.

Sources: [Google: Optimizing for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [Google: Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content), [Google: Link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable).

### P1: add lightweight validation to the publishing path

Keep the current build checks and add a post-build check that fails on:

- a canonical or sitemap URL without a generated file;
- broken internal `<a href>` targets;
- indexable pages with a non-200 public response after deployment;
- invalid JSON-LD syntax or mismatches between structured and visible title, image, author, and dates.

This is important because the Search Console 404 was an old discoverable URL, not a ranking-tuning problem. A sitemap is a discovery hint, not a guarantee, and should contain only canonical URLs. Google also expects standard crawlable links and accurate `lastmod` values.

Source: [Google: SEO guide for developers](https://developers.google.com/search/docs/fundamentals/get-started-developers), [Google: troubleshooting crawling errors](https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors).

### P1: register Bing Webmaster Tools and add IndexNow on publish

1. Verify the GitHub Pages site in Bing Webmaster Tools and submit `https://mchromiak.github.io/sitemap.xml`.
2. Add IndexNow only as a small post-deploy step: host one key file at the site root and submit the URLs added, materially updated, moved, or deleted in that deployment.
3. Do not submit every URL on every build.

Bing strongly recommends IndexNow and says it can accelerate discovery of updates for Bing and participating engines; Bing's guidelines connect current crawl signals to Bing and Copilot grounding. For a small static site this should remain a short deployment step, not a new service.

Sources: [Bing: URL submission](https://www.bing.com/webmasters/help/url-submission-62f2860b), [IndexNow protocol documentation](https://www.indexnow.org/documentation), [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/bing-webmaster-guidelines-30fba23a).

### P2: complete the structured-data presentation already visible on the site

The site already has `BlogPosting`, `WebSite`, and `ProfilePage` markup. The next small corrections are:

1. Change the home-page `WebSite.author.url` from the current relative value `pages/about.html` to the absolute author URL already used by article markup.
2. Add `BreadcrumbList` JSON-LD corresponding to the breadcrumbs already shown to readers on articles and pages.
3. For the most important articles, provide high-resolution representative images in 16:9, 4:3, and 1:1 variants and list them in the article `image` property. Google recommends these three aspect ratios for Article results; this is a recommendation, not a requirement.
4. Run representative URLs through Google's Rich Results Test, then inspect the deployed URL in Search Console.

Structured data can improve Google's understanding and presentation, but Google does not guarantee a rich result and it is not special generative-search markup.

Sources: [Google: Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article), [Google: Breadcrumb structured data](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb), [Google: General structured-data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).

### P2: watch field performance instead of chasing a perfect laboratory score

Use the Search Console Core Web Vitals report for real-user data and work only on failing URL groups. Google's target thresholds are LCP within 2.5 seconds, INP below 200 ms, and CLS below 0.1. The recent image and layout optimization is already the right direction; do not rebuild the theme solely for marginal Lighthouse gains if field data is good.

Source: [Google: Core Web Vitals and Search](https://developers.google.com/search/docs/appearance/core-web-vitals).

## Crawler policy for generative systems

The current `robots.txt` allows all crawlers, so no change is required for discoverability:

- OpenAI says `OAI-SearchBot` must not be blocked if content should be included in ChatGPT Search summaries and snippets.
- Anthropic identifies `Claude-SearchBot` for search and `Claude-User` for user-directed retrieval; both honor `robots.txt`.
- Training crawlers are separate policy choices. Blocking `GPTBot` or `ClaudeBot` while allowing the corresponding search/user crawlers can opt out of future training collection without intentionally removing search access.

This is a rights and distribution decision, not a ranking technique. Explicit `Allow` rules add no benefit while the wildcard rule already allows the site.

Sources: [OpenAI: Publishers and Developers FAQ](https://help.openai.com/en/articles/12627856), [Anthropic: web crawler controls](https://support.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler).

## Practices not supported by current evidence

Do not prioritize these:

- `llms.txt` or a parallel Markdown copy of the site for Google; Google explicitly says it does not use special AI text files for Search.
- FAQ schema on pages that are not genuine FAQ experiences.
- repeating question-answer fragments solely to make artificial "citation chunks".
- mass-changing dates, titles, or summaries without substantive page changes.
- keyword stuffing, purchased mentions, bulk low-quality backlinks, or many thin tag pages.
- promising that schema, IndexNow, or crawler access will produce rankings or AI citations; each improves eligibility or discovery, not guaranteed selection.

Primary source: [Google: Optimizing for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).

## Suggested minimal roadmap

1. **Now:** inspect Search Console Pages/Queries and Core Web Vitals; export a baseline.
2. **Next deployment:** fix the one relative author URL, add breadcrumb JSON-LD, and add the generated-site link/canonical checks.
3. **Next content cycle:** improve the highest-impression underperforming older article and add contextual internal links from its topic cluster.
4. **After that:** register Bing Webmaster Tools and add a minimal changed-URL IndexNow notification.
5. **Measure for 6-8 weeks:** clicks, impressions, CTR, query coverage, engaged sessions, ChatGPT referrals, Bing indexing, and valid rich-result items. Continue only the changes with observable benefit.
