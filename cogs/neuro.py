import re
import time
from random import randint, choice
from datetime import datetime
from collections import deque

import disnake
from disnake.ext import commands

from client import NeuroBot
from message import Message


class Neuro(commands.Cog):
    def __init__(self, bot):
        self.bot: NeuroBot = bot
        self.messages = {}

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.content and not message.content.startswith(('`', '.', ',', '/', '!')) and not message.author.bot:
            if message.channel.id not in self.messages:
                self.messages[message.channel.id] = deque(maxlen=100)

            if content := ''.join(re.findall(r'\w| ', message.content)) in list(map(
                    lambda m: m.content,
                    self.messages[message.channel.id]
            )):
                return

            self.messages[message.channel.id].append(Message(
                guild_id=message.guild.id,
                author_id=message.author.id,
                message_id=message.id,
                content=content,
                datetime=datetime.utcnow()
            ))

        if randint(1, 5) == 1:
            random_message = choice(self.messages[message.channel.id])
            escaped_mentions = disnake.utils.escape_mentions(random_message.content)

            async with message.channel.typing():
                await message.reply(content=escaped_mentions)

    @commands.command(
        name="history",
        aliases=["h"]
    )
    @commands.is_owner()
    async def get_history(self, ctx: commands.Context, *, argument: str = None):
        content = str(self.messages)

        if argument is not None:
            content = self.messages
            for arg in argument.split("/"):
                content = content[eval(arg)]

        if len(content) >= 1992:
            with open("result.txt", "w") as file:
                file.write(content)
                file.close()
            return await ctx.reply(file=disnake.File(
                "result.txt",
                filename=str(time.time()) + ".txt"
            ))

        await ctx.reply(content=content)


def setup(bot):
    bot.add_cog(Neuro(bot))
