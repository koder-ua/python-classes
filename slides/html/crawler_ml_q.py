from threading import Lock, Thread, Queue
from typing import List, Iterator, Tuple


def load_thread(iq: Queue, oq: Queue):
    while True:
        url = iq.get()
        if url is None:
            break
        try:
            data = download_url(url)
            ok = True
        except Exception as exc:
            ok = False
            data = str(exc)
        oq.put((ok, url, data))


def crawl(rool_urls: List[str], nthreads: int = 32) -> Iterator[Tuple[str, str]]:
    used_urls: Set[str] = {}
    url_q = Queue()
    res_q = Queue()

    ths = [Thread(target=load_thread, args=(url_q, res_q)) for _ in range(nthreads)]
    for th in ths:
        th.daemon = True
        th.start()

    waiting_urls = len(rool_urls)
    for url in rool_urls:
        url_q.put(url)

    while waiting_urls:
        ok, url, data = res_q.get()
        waiting_urls -= 1
        if ok:
            waiting_urls += 1
            yield url, data
            for href in find_hrefs(data):
                href = abs_url(href, url)
                if is_beelong_to(href, rool_urls) and url not in used_urls:
                    url_q.append(href)
                    used_url.add(href)
                    waiting_urls += 1

    for url in rool_urls:
        url_q.put(None)

    for th in ths:
        th.join()

