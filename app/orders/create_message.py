import asyncio
import time
from random import randint

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app import orders
from app.loader import dp
from app import config

min_ = 3
max_ = 5


async def send_status_435390():
    list_message = orders.status_435390()
    for message in list_message:
        time.sleep(randint(min_, max_))
        await dp.bot.send_message(chat_id=config.ID_CHANNEL, text=message)


async def send_status_323199():
    list_message = orders.status_323199()
    cnt = 1
    for message in list_message:
        # cnt += 1
        # if cnt % 5 == 0:
        time.sleep(randint(min_, max_))
        await dp.bot.send_message(chat_id=config.ID_CHANNEL, text=message)


async def send_status_435391():
    list_message = orders.status_435391()
    cnt = 1
    for message in list_message:
        # cnt += 1
        # if cnt % 5 == 0:
        time.sleep(randint(min_, max_))
        await dp.bot.send_message(chat_id=config.ID_CHANNEL, text=message)


async def send_status_960847():
    list_message = orders.status_960847()
    cnt = 1
    for message in list_message:
        # cnt += 1
        # if cnt % 5 == 0:
        time.sleep(randint(min_, max_))
        await dp.bot.send_message(chat_id=config.ID_CHANNEL, text=message)


async def send_status_324942():
    list_message = orders.status_324942()
    cnt = 1
    for message in list_message:
        # cnt += 1
        # if cnt % 5 == 0:
        time.sleep(randint(min_, max_))
        await dp.bot.send_message(chat_id=config.ID_CHANNEL, text=message)


async def send_status_355259():
    list_message = orders.status_355259()
    cnt = 1
    for message in list_message:
        # cnt += 1
        # if cnt % 5 == 0:
        time.sleep(randint(min_, max_))
        await dp.bot.send_message(chat_id=config.ID_CHANNEL, text=message)


async def send_status_349784():
    list_message = orders.status_349784()
    cnt = 1
    for message in list_message:
        # cnt += 1
        # if cnt % 5 == 0:
        time.sleep(randint(min_, max_))
        await dp.bot.send_message(chat_id=config.ID_CHANNEL, text=message)


async def send_status_349471():
    list_message = orders.status_349471()
    cnt = 1
    for message in list_message:
        # cnt += 1
        # if cnt % 5 == 0:
        time.sleep(randint(min_, max_))
        await dp.bot.send_message(chat_id=config.ID_CHANNEL, text=message)


async def send_status_325119():
    list_message = orders.status_325119()
    for message in list_message:
        time.sleep(randint(min_, max_))
        await dp.bot.send_message(chat_id=config.ID_CHANNEL, text=message)


async def send_status_324856():
    list_message = orders.status_324856()
    for message in list_message:
        time.sleep(randint(min_, max_))
        await dp.bot.send_message(chat_id=config.ID_CHANNEL, text=message)


async def hand_send():
    await send_status_435390()
    await send_status_323199()
    await send_status_435391()
    await send_status_960847()
    await send_status_324942()
    await send_status_355259()
    await send_status_349784()
    await send_status_349471()
    await send_status_325119()
    await send_status_324856()


scheduler = AsyncIOScheduler()

scheduler.add_job(send_status_435390, 'interval', hours=2)
scheduler.add_job(send_status_323199, 'interval', minutes=10)
scheduler.add_job(send_status_349471, 'interval', hours=1)
scheduler.add_job(send_status_435391, 'cron', hour=14)
scheduler.add_job(send_status_435391, 'cron', hour=16)
scheduler.add_job(send_status_435391, 'cron', hour=18)
scheduler.add_job(send_status_435391, 'cron', hour=20)
scheduler.add_job(send_status_960847, 'cron', hour=9)
scheduler.add_job(send_status_960847, 'cron', hour=13)
scheduler.add_job(send_status_960847, 'cron', hour=17)
scheduler.add_job(send_status_960847, 'cron', hour=21)
scheduler.add_job(send_status_324942, 'cron', hour=9)
scheduler.add_job(send_status_324942, 'cron', hour=13)
scheduler.add_job(send_status_324942, 'cron', hour=17)
scheduler.add_job(send_status_324942, 'cron', hour=21)
scheduler.add_job(send_status_324942, 'cron', hour=23)
scheduler.add_job(send_status_355259, 'cron', hour=17)
scheduler.add_job(send_status_355259, 'cron', hour=22)
scheduler.add_job(send_status_349784, 'cron', hour=17)
scheduler.add_job(send_status_349784, 'cron', hour=22)
scheduler.add_job(send_status_324856, 'cron', hour=9)
scheduler.add_job(send_status_324856, 'cron', hour=19)
scheduler.add_job(send_status_325119, 'cron', hour=9)
scheduler.add_job(send_status_325119, 'cron', hour=12)
scheduler.add_job(send_status_325119, 'cron', hour=17)
scheduler.add_job(send_status_325119, 'cron', hour=21)
