from cachetools import TTLCache

from tgbot.config import config

throttling_cache = TTLCache(maxsize=10_000, ttl=config.rate_limit)