from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag


def parse_page(html, base_url):

    soup = BeautifulSoup(html, "html.parser")


    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg"
    ]):
        tag.decompose()

    title = ""

    if soup.title:
        title = soup.title.get_text(
            " ",
            strip=True
        )

    content = soup.get_text(
        " ",
        strip=True
    )

    links = []

    for a in soup.find_all("a", href=True):

        href = a["href"].strip()

        # Convert relative URL → absolute URL
        absolute = urljoin(
            base_url,
            href
        )

        # Remove #fragment
        absolute, _ = urldefrag(
            absolute
        )

        if absolute.startswith(
            ("http://", "https://")
        ):
            links.append(absolute)

    return {
        "title": title,
        "content": content,
        "links": links
    }