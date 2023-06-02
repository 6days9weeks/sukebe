# pylint: disable=missing-module-docstring
import math
import random
import time
from contextlib import suppress
from io import BytesIO
from pathlib import Path
from typing import List

from loguru import logger  # pylint: disable=import-error

from sukebe.utils import (
    HTTPClient,
    avatars,
    danbooru_tags,
    konachan_tags,
    lunar_tags,
    nekoslife_tags,
    subreddits,
    waifu_im_tags,
    yandere_tags,
)


def load_webhooks() -> List[str]:
    """Load webhooks from webhooks.txt"""
    logger.info("Loading webhooks...")
    with open(  # pylint: disable=unspecified-encoding
        Path.cwd() / "webhooks.txt", "r"
    ) as f:  # pylint: disable=invalid-name
        return [x.strip() for x in f.readlines()]


def send_webhook(webhook: str, type_: str, name: str, file: BytesIO, client: HTTPClient) -> None:
    """Send files to discord webhook"""
    client.session.post(
        url=webhook,
        data={
            "username": "sukebe",
            "avatar_url": avatars[math.floor(random.random() * len(avatars))],
        },
        files={"upload-file": (f"{name}-{type_}.png", file)},
    )


def loop_reddit(  # pylint: disable=missing-function-docstring
    webhooks: List[str], http: HTTPClient
) -> None:
    for subreddit in subreddits:
        logger.info(f"Getting image from {subreddit}...")
        image = http.get_reddit(subreddit)
        if not image:
            logger.error(f"Failed to get image from {subreddit}")
            continue
        logger.info(f"Sending image from {subreddit}...")
        file = BytesIO(http.session.get(image).content)
        for webhook in webhooks:
            send_webhook(webhook, "reddit", subreddit, file, http)
            time.sleep(0.5)
        time.sleep(5)


def loop_yandere(  # pylint: disable=missing-function-docstring
    webhooks: List[str], http: HTTPClient
) -> None:
    for tag in yandere_tags:
        logger.info(f"Getting image from yandere with tag {tag}...")
        image = http.get_yandere(tag)
        if not image:
            logger.error(f"Failed to get image from yandere with tag {tag}")
            continue
        logger.info(f"Sending image from yandere with tag {tag}...")
        file = BytesIO(http.session.get(image).content)
        for webhook in webhooks:
            send_webhook(webhook, "yandere", tag, file, http)
            time.sleep(0.5)
        time.sleep(5)


def loop_nekoslife(  # pylint: disable=missing-function-docstring
    webhooks: List[str], http: HTTPClient
) -> None:
    for tag in nekoslife_tags:
        logger.info(f"Getting image from nekos.life with tag {tag}...")
        image = http.get_nekos(tag)
        if not image:
            logger.error(f"Failed to get image from nekos.life with tag {tag}")
            continue
        logger.info(f"Sending image from nekos.life with tag {tag}...")
        file = BytesIO(http.session.get(image).content)
        for webhook in webhooks:
            send_webhook(webhook, "nekos.life", tag, file, http)
            time.sleep(0.5)
        time.sleep(5)


def loop_danbooru(  # pylint: disable=missing-function-docstring
    webhooks: List[str], http: HTTPClient
) -> None:
    for tag in danbooru_tags:
        logger.info(f"Getting image from danbooru with tag {tag}...")
        image = http.get_danbooru(tag)
        if not image:
            logger.error(f"Failed to get image from danbooru with tag {tag}")
            continue
        logger.info(f"Sending image from danbooru with tag {tag}...")
        file = BytesIO(http.session.get(image).content)
        for webhook in webhooks:
            send_webhook(webhook, "danbooru", tag, file, http)
            time.sleep(0.5)
        time.sleep(5)


def loop_konachan(  # pylint: disable=missing-function-docstring
    webhooks: List[str], http: HTTPClient
) -> None:
    for tag in konachan_tags:
        logger.info(f"Getting image from konachan with tag {tag}...")
        image = http.get_konachan(tag)
        if not image:
            logger.error(f"Failed to get image from konachan with tag {tag}")
            continue
        logger.info(f"Sending image from konachan with tag {tag}...")
        file = BytesIO(http.session.get(image).content)
        for webhook in webhooks:
            send_webhook(webhook, "konachan", tag, file, http)
            time.sleep(0.5)
        time.sleep(5)


def loop_lunar(  # pylint: disable=missing-function-docstring
    webhooks: List[str], http: HTTPClient
) -> None:
    for tag in lunar_tags:
        logger.info(f"Getting image from lunar with tag {tag}...")
        image = http.get_lunar(tag)
        if not image:
            logger.error(f"Failed to get image from lunar with tag {tag}")
            continue
        logger.info(f"Sending image from lunar with tag {tag}...")
        file = BytesIO(http.session.get(image).content)
        for webhook in webhooks:
            send_webhook(webhook, "lunar", tag, file, http)
            time.sleep(0.5)
        time.sleep(5)


def loop_waifu_im(  # pylint: disable=missing-function-docstring
    webhooks: List[str], http: HTTPClient
) -> None:
    for tag in waifu_im_tags:
        logger.info(f"Getting image from waifu.im with tag {tag}...")
        image = http.get_waifu_im(tag)
        if not image:
            logger.error(f"Failed to get image from waifu.im with tag {tag}")
            continue
        logger.info(f"Sending image from waifu.im with tag {tag}...")
        file = BytesIO(http.session.get(image).content)
        for webhook in webhooks:
            send_webhook(webhook, "waifu.im", tag, file, http)
            time.sleep(0.5)
        time.sleep(5)


def loop(  # pylint: disable=missing-function-docstring
    webhooks: List[str], http: HTTPClient
) -> None:
    logger.info("Starting loop...")
    while True:
        with suppress(Exception):
            logger.info("Iterating...")
            loop_lunar(webhooks, http)
            loop_waifu_im(webhooks, http)
            loop_reddit(webhooks, http)
            loop_yandere(webhooks, http)
            loop_nekoslife(webhooks, http)
            loop_danbooru(webhooks, http)
            loop_konachan(webhooks, http)
            logger.info("Finished iterating, sleeping for 30 minutes...")
            time.sleep(http.config.wait)
