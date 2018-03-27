from concurrent.futures import ThreadPoolExecutor
from typing import List, Iterator, Tuple


def load_thread(url):
    return url, download_url(url)


def crawl(rool_urls: List[str], nthreads: int = 32) -> Iterator[Tuple[str, str]]:
    used_urls: Set[str] = {}

    with ThreadPoolExecutor(max_workers=nthreads) as pool:
        futures = [pool.submit(load_thread, url) for url in rool_urls]
        while futures:
            (ready_future,), futures = concurrent.futures.wait(futures, return_when=FIRST_COMPLETED)
            url, data = ready_future.result()
            yield url, data
            for href in find_hrefs(data):
                href = abs_url(href, url)
                if is_beelong_to(href, rool_urls) and url not in used_urls:
                    futures.append(pool.submit(load_thread, href))
                    used_url.add(href)


