from disnake import Intents
from disnake.ext.commands import Bot


def get_history() -> dict:
    return __import__("cogs.neuro").Neuro().messages


class NeuroBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=['.', ','],
            intents=Intents.all(),
            *args,
            **kwargs
        )

