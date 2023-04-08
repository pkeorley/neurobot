from client import NeuroBot
from config import data

bot = NeuroBot()


@bot.event
async def on_ready():
    try:
        bot.load_extensions("cogs")
    except Exception as error:
        print(f"[Cog] {error}")
    print(bot.user, "on ready!")


bot.run(data["token"])
