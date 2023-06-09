# pylint: disable=missing-module-docstring
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Union

import httpx  # pylint: disable=import-error
from loguru import logger  # pylint: disable=import-error


@dataclass
class Config:
    """Config class for sukebe"""

    wait: int
    lunar_token: str

    @classmethod
    def from_disk(cls) -> "Config":
        """Create a Config object from a json file"""
        with open( # pylint: disable=unspecified-encoding,
            Path.cwd() / "config.json", "r"
        ) as f:  # pylint: disable=invalid-name
            data = json.load(f)
        return cls(**data)


class HTTPClient:
    """Base HTTP client for sukebe"""

    def __init__(self) -> None:
        self.session = httpx.Client()
        self.config = Config.from_disk()
        self.base_urls: Dict[str, str] = {
            "reddit": "https://www.reddit.com/r/{}/hot.json?limit=100",
            "danbooru": "https://danbooru.donmai.us/posts.json?tags={}&limit=200",
            "nekos.life": "https://nekos.life/api/v2/img/{}",
            "konachan": "https://konachan.com/post.json?tags={}&limit=500",
            "yandere": "https://yande.re/post.json?tags={}&limit=500",
            "lunar": "https://api.lunardev.group/nsfw/{}",
            "waifu.im": "https://api.waifu.im/search?included_tags={}&is_nsfw=true&gif=false",
        }

    def get_reddit(self, subreddit: str) -> Union[None, str]:  # pylint: disable=missing-function-docstring
        url = self.base_urls["reddit"].format(subreddit)
        logger.debug(f"GET {url}")
        r = self.session.get(url)  # pylint: disable=invalid-name
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

    def get_nekos(self, tag: str) -> Union[None, str]:  # pylint: disable=missing-function-docstring
        url = self.base_urls["nekos.life"].format(tag)
        logger.debug(f"GET {url}")
        r = self.session.get(url)  # pylint: disable=invalid-name
        if r.status_code != 200:
            logger.error(f"GET {url} returned {r.status_code}")
            return
        return r.json()["url"]

    def get_danbooru(self, tag: str) -> Union[None, str]:  # pylint: disable=missing-function-docstring
        url = self.base_urls["danbooru"].format(tag)
        logger.debug(f"GET {url}")
        r = self.session.get(url)  # pylint: disable=invalid-name
        if r.status_code != 200:
            logger.error(f"GET {url} returned {r.status_code}")
            return
        all_posts = r.json()
        filtered_posts = [
            x for x in all_posts if x["rating"] != "s" and "trap" not in x["tag_string"]
        ]
        return filtered_posts[math.floor(random.random() * len(filtered_posts))]["file_url"]

    def get_konachan(self, tag: str) -> Union[None, str]:  # pylint: disable=missing-function-docstring
        url = self.base_urls["konachan"].format(tag)
        logger.debug(f"GET {url}")
        r = self.session.get(url)  # pylint: disable=invalid-name
        if r.status_code != 200:
            logger.error(f"GET {url} returned {r.status_code}")
            return
        all_posts = r.json()
        filtered_posts = [x for x in all_posts if x["rating"] != "s" and "trap" not in x["tags"]]
        return filtered_posts[math.floor(random.random() * len(filtered_posts))]["file_url"]

    def get_yandere(self, tag: str) -> Union[None, str]:  # pylint: disable=missing-function-docstring
        url = self.base_urls["yandere"].format(tag)
        logger.debug(f"GET {url}")
        r = self.session.get(url)  # pylint: disable=invalid-name
        if r.status_code != 200:
            logger.error(f"GET {url} returned {r.status_code}")
            return
        all_posts = r.json()
        filtered_posts = [x for x in all_posts if x["rating"] != "s" and "trap" not in x["tags"]]
        return filtered_posts[math.floor(random.random() * len(filtered_posts))]["file_url"]

    def get_lunar(self, tag: str) -> Union[None, str]:  # pylint: disable=missing-function-docstring
        url = self.base_urls["lunar"].format(tag)
        logger.debug(f"GET {url}")
        headers = {"Authorization": self.config.lunar_token}
        r = self.session.get(url, headers=headers)  # pylint: disable=invalid-name
        if r.status_code != 200:
            logger.error(f"GET {url} returned {r.status_code}")
            return
        data = r.json()
        if ".gif" in data["name"]:
            return
        return data["url"]

    def get_waifu_im(self, tag: str) -> Union[None, str]:  # pylint: disable=missing-function-docstring
        url = self.base_urls["waifu.im"].format(tag)
        logger.debug(f"GET {url}")
        r = self.session.get(url)  # pylint: disable=invalid-name
        if r.status_code != 200:
            logger.error(f"GET {url} returned {r.status_code}")
            return
        return r.json()["images"][0]["url"]
