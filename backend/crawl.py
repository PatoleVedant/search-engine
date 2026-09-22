from app.database.db import init_db
from app.crawler.crawler import Crawler


def main():

    # init_db()

    seed_url = input(
        "Enter seed URL: "
    ).strip()

    crawler = Crawler(
        seed_url
    )

    crawler.crawl()


if __name__ == "__main__":
    main()