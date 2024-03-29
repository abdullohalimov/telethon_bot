from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from tgbot.services.cache import throttling_cache


class ThrottlingMiddleware(BaseMiddleware):
    cache = throttling_cache

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.id not in self.cache.keys():
            self.cache[event.chat.id] = None
            return await handler(event, data)

        return