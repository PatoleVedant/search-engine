from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse


class RobotsManager:

    def __init__(self):

        self.parsers = {}

    def get_parser(self, url):

        parsed = urlparse(url)

        origin = (
            f"{parsed.scheme}://"
            f"{parsed.netloc}"
        )

        if origin in self.parsers:
            return self.parsers[origin]

        robots_url = (
            f"{origin}/robots.txt"
        )

        parser = RobotFileParser(
            robots_url
        )

        try:
            parser.read()
        except Exception:
            return None

        self.parsers[origin] = parser

        return parser

    def allowed(self, url, user_agent):

        parser = self.get_parser(url)

        if parser is None:
            return False

        return parser.can_fetch(
            user_agent,
            url
        )