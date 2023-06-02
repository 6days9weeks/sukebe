import math
import random
from typing import Dict

import httpx  # pylint: disable=import-error
from loguru import logger  # pylint: disable=import-error


class HTTPClient:
    """Base HTTP client for sukebe"""

    def __init__(self) -> None:
        self.session = httpx.Client()
        self.base_urls: Dict[str, str] = {
            "reddit": "https://www.reddit.com/r/{}/hot.json?limit=100",
            "danbooru": "https://danbooru.donmai.us/posts.json?tags={}&limit=200",
            "nekos.life": "https://nekos.life/api/v2/img/{}",
            "konachan": "https://konachan.com/post.json?tags={}&limit=500",
            "yandere": "https://yande.re/post.json?tags={}&limit=500",
        }

    def get_reddit(self, subreddit: str) -> str:
        url = self.base_urls["reddit"].format(subreddit)
        logger.debug(f"GET {url}")
        r = self.session.get(url)
        if r.status_code != 200:
            logger.error(f"GET {url} returned {r.status_code}")
            return
        all_posts = r.json()
        filtered_posts = [
            x
            for x in all_posts["data"]["children"]
            if "post_hint" in x["data"].keys() and x["data"]["post_hint"] == "image"
        ]
        return filtered_posts[math.floor(random.random() * len(filtered_posts))]["data"]["url"]

    def get_nekos(self, tag: str) -> str:
        url = self.base_urls["nekos.life"].format(tag)
        logger.debug(f"GET {url}")
        r = self.session.get(url)
        if r.status_code != 200:
            logger.error(f"GET {url} returned {r.status_code}")
            return
        return r.json()["url"]

    def get_danbooru(self, tag: str) -> str:
        url = self.base_urls["danbooru"].format(tag)
        logger.debug(f"GET {url}")
        r = self.session.get(url)
        if r.status_code != 200:
            logger.error(f"GET {url} returned {r.status_code}")
            return
        all_posts = r.json()
        filtered_posts = [
            x for x in all_posts if x["rating"] != "s" and "trap" not in x["tag_string"]
        ]
        return filtered_posts[math.floor(random.random() * len(filtered_posts))]["file_url"]

    def get_konachan(self, tag: str) -> str:
        url = self.base_urls["konachan"].format(tag)
        logger.debug(f"GET {url}")
        r = self.session.get(url)
        if r.status_code != 200:
            logger.error(f"GET {url} returned {r.status_code}")
            return
        all_posts = r.json()
        filtered_posts = [x for x in all_posts if x["rating"] != "s" and "trap" not in x["tags"]]
        return filtered_posts[math.floor(random.random() * len(filtered_posts))]["file_url"]

    def get_yandere(self, tag: str) -> str:
        url = self.base_urls["yandere"].format(tag)
        logger.debug(f"GET {url}")
        r = self.session.get(url)
        if r.status_code != 200:
            logger.error(f"GET {url} returned {r.status_code}")
            return
        all_posts = r.json()
        filtered_posts = [x for x in all_posts if x["rating"] != "s" and "trap" not in x["tags"]]
        return filtered_posts[math.floor(random.random() * len(filtered_posts))]["file_url"]
