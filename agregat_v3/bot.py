import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.handlers.admin import admin_router
from tgbot.handlers.callback import custom_router, custom_router2
from tgbot.middlewares.album import MediaGroupMiddleware 
from tgbot.middlewares.throttling import ThrottlingMiddleware 
from tgbot.services import broadcaster

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот был запущен")


def register_global_middlewares(dp: Dispatcher, config):
    # dp.message.outer_middleware(MediaGroupMiddleware)
    # dp.message.outer_middleware(ConfigMiddleware(config=config))
    dp.message.outer_middleware(ThrottlingMiddleware())
    dp.message.middleware(MediaGroupMiddleware())
    # dp.callback_query.outer_middleware(ConfigMiddleware(config))
    


async def main():
    logging.basicConfig(
        level=logging.WARNING,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(message)s',
    )
    logger.critical("Starting bot")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='Markdown')
    dp = Dispatcher(storage=storage)

    for router in [
        custom_router,
        admin_router,
        custom_router2
    ]:
        dp.include_router(router)

    register_global_middlewares(dp, config)

    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот был выключен!")
