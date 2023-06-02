# pylint: disable=missing-module-docstring
import os
from pathlib import Path
import sys

from loguru import logger  # pylint: disable=import-error

from sukebe import HTTPClient, load_webhooks, loop

if __name__ == "__main__":
    logger.info("Starting sukebe...")
    if not os.path.exists(Path.cwd() / "config.json"):
        logger.error("config.json not found!")
        sys.exit(1)
    if not os.path.exists(Path.cwd() / "webhooks.txt"):
        logger.error("webhooks.txt not found!")
        sys.exit(1)
    hooks = load_webhooks()
    session = HTTPClient()
    try:
        loop(hooks, session)
    except KeyboardInterrupt:
        logger.info("Exiting...")
        sys.exit(0)
