import discord
from discord.ext import commands
import asyncio
import itertools

class Events(commands.Cog, name='Events'):

    def __init__(self, bot):
        self.bot = bot
        self.owo_cache = []
        self.hunt_cache = []
        self.battle_cache = []
        self.STATUS = itertools.cycle(["a", "b"])

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
            
        if ctx.content.startswith("owoh") or ctx.content.startswith("owohunt") or ctx.content.startswith("owocatch"):
            
            if ctx.author.id not in self.hunt_cache:
                self.hunt_cache.append(ctx.author.id)
                await self.bot.hdb.add_count(ctx.author.id, "hunt")
                
                await asyncio.sleep(15)
                await ctx.channel.send("time for hunting")
                
                self.hunt_cache.remove(ctx.author.id)
                
                
        elif ctx.content.startswith("owob") or ctx.content.startswith("owobattle") or ctx.content.startswith("owofight"):
            
            if ctx.author.id not in self.battle_cache:
                
                self.battle_cache.append(ctx.author.id)
                await self.bot.hdb.add_count(ctx.author.id, "battle")

                await asyncio.sleep(15)
                await ctx.channel.send("time for battling")
                
                self.battle_cache.remove(ctx.author.id)
                

        elif ("owo" in ctx.content) or ("uwu" in ctx.content):
            
            for name in self.bot.t.command_names:
                
                if ctx.content.startswith(f"owo{name}"):
                    print(f"recognized owo{name}")
                    return

                if ctx.content.startswith(f"uwu{name}"):
                    print(f"recognized uwu{name}")
                    return
                    
            if ctx.author.id not in self.owo_cache:
                
                self.owo_cache.append(ctx.author.id)
                await self.bot.hdb.add_count(ctx.author.id, "owo")

                await asyncio.sleep(10)
                await ctx.channel.send("time for o-wo")
                
                self.owo_cache.remove(ctx.author.id)

        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if self.bot.d.verification_msg_id == payload.message_id:
            
            channel = self.bot.get_channel(payload.channel_id)
            await channel.send("verified")

            member = self.bot.d.bhv.get_member(payload.user_id)
            await member.add_roles(*self.bot.d.verify_roles)

        
def setup(bot):
    bot.add_cog(Events(bot))