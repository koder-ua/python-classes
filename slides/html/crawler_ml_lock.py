from threading import Lock, Thread
from typing import List, Iterator, Tuple


class CrawlThread(Thread):
    def __init__(self, root_urls: List[str],
                 curr_urls: List[str], curr_lock: Lock,
                 used_urls: Set[str], used_lock: Lock,
                 results: List[Tuple[str, str]], result_lock: Lock) -> None:
        Thread.__init__(self)
        self.daemon = True

        self.root_urls = root_urls

        self.curr_urls = curr_urls
        self.curr_lock = curr_lock

        self.used_urls = used_urls
        self.used_lock = used_lock
        self.results = results
        self.result_lock = result_lock

    def run(self):
        while True:
            with self.curr_lock:
                if not self.curr_urls:
                    break
                url = self.curr_urls.pop()

            data = download_url(url)
            for href in find_hrefs(data):
                href = abs_url(href, url)
                if is_beelong_to(href, self.rool_urls):
                    with self.used_lock:
                        if url not in self.used_urls:
                            with self.curr_lock:
                                self.curr_urls.append(href)
                            self.used_url.add(href)



def crawl(rool_urls: List[str], nthreads: int = 32) -> Iterator[Tuple[str, str]]:
    used_urls: Set[str] = {}
    curr_urls = rool_urls[:]
    used_lock = Lock()
    curr_lock = Lock()
    results: List[Tuple[str, str]] = []
    results_lock = Lock()

    ths = [CrawlThread(rool_urls,
                       curr_urls=curr_urls, curr_lock=curr_lock,
                       user_urls=used_urls, used_lock=curr_lock,
                       results=results, results_lock=results_lock)
           for _ in range(nthreads)]

    for th in ths:
        th.start()

    any_running = True
    while any_running:
        time.sleep(0.1)
        with results_lock:
            yield from results
            # results = [] <<< wrong
            results.clear()

        any_running = any(th.is_alive() for th in ths)


