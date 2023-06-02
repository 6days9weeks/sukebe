import math
import random
import time
from contextlib import suppress
from io import BytesIO
from pathlib import Path
from typing import List

from loguru import logger

from sukebe.utils import (
    HTTPClient,
    avatars,
    danbooru_tags,
    konachan_tags,
    nekoslife_tags,
    subreddits,
    yandere_tags,
)


def load_webhooks() -> List[str]:
    """Load webhooks from webhooks.txt"""
    logger.info("Loading webhooks...")
    with open(Path.cwd() / "webhooks.txt", "r") as f:
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


def loop_reddit(webhooks: List[str], http: HTTPClient) -> None:
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


def loop_yandere(webhooks: List[str], http: HTTPClient) -> None:
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


def loop_nekoslife(webhooks: List[str], http: HTTPClient) -> None:
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


def loop_danbooru(webhooks: List[str], http: HTTPClient) -> None:
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


def loop_konachan(webhooks: List[str], http: HTTPClient) -> None:
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


def loop(webhooks: List[str], http: HTTPClient) -> None:
    logger.info("Starting loop...")
    while True:
        with suppress(Exception):
            logger.info("Iterating...")
            loop_reddit(webhooks, http)
            loop_yandere(webhooks, http)
            loop_nekoslife(webhooks, http)
            loop_danbooru(webhooks, http)
            loop_konachan(webhooks, http)
            logger.info("Finished iterating, sleeping for 30 minutes...")
            time.sleep(1800)
