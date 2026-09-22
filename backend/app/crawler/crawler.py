import hashlib
import time

import requests

from collections import deque
from urllib.parse import urlparse

from .parser import parse_page
from .robots import RobotsManager

from app.database.db import save_document


USER_AGENT = "MySearchEngineBot/0.1"

MAX_PAGES = 200

REQUEST_DELAY = 1.5


class Crawler:

    def __init__(self, seed_url):

        self.seed_url = seed_url

        self.queue = deque([
            seed_url
        ])

        self.visited = set()

        self.robots = RobotsManager()

        parsed = urlparse(seed_url)

        self.allowed_domain = (
            parsed.netloc
        )

    def same_domain(self, url):

        return (
            urlparse(url).netloc
            == self.allowed_domain
        )

    def crawl(self):

        while (
            self.queue
            and len(self.visited) < MAX_PAGES
        ):

            url = self.queue.popleft()

            if url in self.visited:
                continue

            if not self.same_domain(url):
                continue

            self.visited.add(url)

            # Respect robots.txt
            if not self.robots.allowed(
                url,
                USER_AGENT
            ):
                print(
                    f"Blocked by robots.txt: {url}"
                )

                continue

            try:

                print(
                    f"[{len(self.visited)}] "
                    f"Crawling {url}"
                )

                response = requests.get(
                    url,
                    headers={
                        "User-Agent":
                            USER_AGENT
                    },
                    timeout=10
                )

                if response.status_code != 200:
                    continue

                content_type = (
                    response.headers
                    .get(
                        "Content-Type",
                        ""
                    )
                )

                if "text/html" not in content_type:
                    continue

                page = parse_page(
                    response.text,
                    url
                )

                content = page["content"]

                content_hash = hashlib.sha256(
                    content.encode("utf-8")
                ).hexdigest()

                save_document(
                    url,
                    page["title"],
                    content,
                    content_hash
                )

                # Add new URLs
                for link in page["links"]:

                    if (
                        link not in self.visited
                        and self.same_domain(link)
                    ):
                        self.queue.append(
                            link
                        )

            except requests.RequestException as e:

                print(
                    f"Request failed: {e}"
                )

            # POLITE DELAY
            time.sleep(
                REQUEST_DELAY
            )