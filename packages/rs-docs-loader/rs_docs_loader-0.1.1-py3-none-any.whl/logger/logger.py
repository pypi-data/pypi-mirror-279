import logging

from global_config import LOG_LEVEL

logger = logging.getLogger(__name__)


def set_log_level():
    logging.basicConfig(level=LOG_LEVEL)
