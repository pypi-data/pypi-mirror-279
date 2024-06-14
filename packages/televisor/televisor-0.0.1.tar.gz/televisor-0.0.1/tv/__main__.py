from os import getenv
from click import group, argument
from telegram.ext import Application
import asyncio

chat_id = getenv('MY_CHAT_ID')
token = getenv('TELEVISOR_TOKEN')


@group()
def main():
    pass


async def send_video(app, file):
    await app.bot.send_video(chat_id, file)


@main.command()
@argument('path', type = str, default = '/home/zeio/recording.mp4')
def send(path: str):
    app = Application.builder().token(token).build()

    with open(path, 'rb') as file:
        asyncio.run(send_video(app, file))


if __name__ == '__main__':
    main()
