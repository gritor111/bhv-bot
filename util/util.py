import discord


class Util():

    def __init__(self, bot) -> None:
        self.bot = bot

    async def send(self, ctx, message, color="#f77394"):
        embed = discord.Embed(color=discord.Colour.from_str(color), description=message)
        await ctx.channel.send(embed=embed)


def setup(bot):
    return Util(bot)