import logging
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

API_TOKEN = "5265833643:AAGjzE0nqHVX5la_N8Ixf8y6O2HSnABTGuI"

whk_hst = 'https://examle.com'
whk_pth = '/path/to/api'
whk_url = f'{whk_hst}{whk_pth}'

wbp_hst = 'localhost'
wbp_prt = 3001

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler()

async def echo(message:types.Message):
    return SendMessage(message.chat.id, message.text)

async def on_startup(dp):
    await bot.set_webhook((whk_url))

async def on_shutdown(dp):
    logging.warning('Отключаем')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Пока')

if __name__ == '__main__':
    start_webhook(
    dispatcher=dp,
    webhook_path=whk_pth,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host=wbp_hst,
    port=wbp_prt
 )