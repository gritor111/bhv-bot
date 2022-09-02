from util.setup import get_time
from discord.ext import commands
import datetime

class Stats(commands.Cog, name='Stats'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats", aliases=["s"])
    async def stats(self, ctx, type=None, time="all_time"):
        
        user_count = (await self.bot.hdb.get_user_count(ctx.author.id, get_time(time)))[0]

        score = 0
        for type in ["owo", "hunt", "battle"]:
            score += user_count[type]
            await ctx.channel.send(f"{type} count: {user_count[type]}")

        await ctx.channel.send("score: " + str(score/3))  # avg
            
    
async def setup(bot):
    await bot.add_cog(Stats(bot))