def crawl(rool_urls: List[str]) -> Iterator[Tuple[str, str]]:
    used_urls: Set[str] = {}
    curr_urls = rool_urls[:]
    while urls:
        url = urls[-1]
        data = download_url(url)
        yield url, data
        for href in find_hrefs(data):
            href = abs_url(href, url)
            if is_beelong_to(href, rool_urls) and url not in used_urls:
                root_urls.append(href)
                used_url.add(href)
