from loguru import logger  # pylint: disable=import-error

from sukebe.utils import HTTPClient, load_webhooks, loop

if __name__ == "__main__":
    logger.info("Starting sukebe...")
    hooks = load_webhooks()
    session = HTTPClient()
    try:
        loop(hooks, session)
    except KeyboardInterrupt:
        logger.info("Exiting...")
        exit(0)
