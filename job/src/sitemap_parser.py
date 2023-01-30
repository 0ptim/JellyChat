from usp.tree import sitemap_tree_for_homepage


def getUrlsToScrape(rootUrl: str):
    print('🔎 Scanning "%s" for pages to scrape' % rootUrl)
    tree = sitemap_tree_for_homepage(rootUrl)
    urls = list()
    for page in tree.all_pages():
        print('📃 Found page:', page.url)
        urls.append(page.url)
    urls = list(set(urls))  # Remove duplicates
    return urls
