import logging
import os
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook


api_tok = os.getenv('bot_tok')
bot = Bot(token = api_tok)
dp = Dispatcher(bot)

her_app_nam = os.getenv('her_app_nam')

whk_hst = f'https://{her_app_nam}.herokuapp.com'
whk_pth = f'/webhook/{api_tok}'
whk_url = f'{whk_hst}{whk_pth}'

wbp_hst = '0.0.0.0'
wbp_prt = os.getenv('port', default = 8000)

logging.basicConfig(level=logging.INFO)
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