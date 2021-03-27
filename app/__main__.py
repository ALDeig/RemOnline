from aiogram import Dispatcher
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app import utils, config
from app.loader import dp
from app import orders

# The configuration of the modules using import
from app import middlewares, filters, handlers


async def on_startup(dispatcher: Dispatcher):
    await utils.setup_default_commands(dispatcher)
    await utils.notify_admins(config.ADMIN_IDS)


# async def send_status_435390():
#     list_message = orders.status_435390()
#     for message in list_message:
#         await dp.bot.send_message(chat_id=config.ADMIN_IDS[0], text=message)


if __name__ == '__main__':
    utils.setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api"])
    orders.scheduler.start()
    executor.start_polling(
        dp, on_startup=on_startup, skip_updates=config.SKIP_UPDATES
    )
