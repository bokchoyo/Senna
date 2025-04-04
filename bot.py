import asyncio
import os
import signal
import time
import discord
from orjson import orjson
from helpers.config import Config
from discord.ext import commands
from handlers.users import Users
from handlers.cars import Cars
from handlers.garages import Garages

class Bot(commands.Bot):
    def __init__(self, configurator, **kwargs):
        super().__init__(**kwargs)
        self.embed_color = configurator.get_embed_color()
        self.attachment_head = configurator.get_attachment_head()
        self.user_db = Users()
        self.car_db = Cars()
        self.garage_db = Garages()
        self.spec_options = {}
        self.makes = []

    async def setup_hook(self):
        self.makes = await self.car_db.get_makes()
        self.load_extension('cogs.specs')
        await self.sync_commands()

    async def on_ready(self):
        print(f'Successfully logged in as {self.user}')
        await self.setup_hook()
        print(f'Initialized')

    async def close(self):
        print("Closing cogs...")

        cog = self.get_cog('Specs')
        if cog:
            cog.close()
        else:
            print("Specs Cog not found")
        await super().close()

    def close_cogs(self):
        cog = self.get_cog('Specs')
        if cog:
            cog.close()
        else:
            print("Specs Cog not found")

    async def cleanup(self):
        # Clean up any remaining resources, such as the aiohttp session
        await self.http.close()

async def main():
    config = Config()
    bot = Bot(config, intents=discord.Intents.all())
    try:
        # Start the bot
        await bot.start(config.get_bot_token())
    except (asyncio.CancelledError, KeyboardInterrupt, SystemExit):
        # Handle graceful shutdown if interrupted or terminated
        print("Bot is shutting down...")
        await bot.close()
        await bot.cleanup()

if __name__ == '__main__':
    asyncio.run(main())