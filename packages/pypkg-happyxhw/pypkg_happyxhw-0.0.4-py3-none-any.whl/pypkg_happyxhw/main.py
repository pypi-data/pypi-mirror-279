import logging

from setup_logging import setup

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    setup()
    logger.info("logger set :D")
    logger.error("logger set :D")
