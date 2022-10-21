import discord
from discord.ext import commands
import asyncio
import itertools

BAD_ARG_ERRORS = (
    commands.BadArgument,
    commands.errors.UnexpectedQuoteError,
    commands.errors.ExpectedClosingQuoteError,
    commands.errors.BadUnionArgument,
)

IGNORED_ERRORS = (commands.CommandNotFound, commands.NotOwner)


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

                self.hunt_cache.remove(ctx.author.id)
                
                
        elif ctx.content.startswith("owob") or ctx.content.startswith("owobattle") or ctx.content.startswith("owofight"):
            
            if ctx.author.id not in self.battle_cache:
                
                self.battle_cache.append(ctx.author.id)
                await self.bot.hdb.add_count(ctx.author.id, "battle")

                await asyncio.sleep(15)

                self.battle_cache.remove(ctx.author.id)
                

        elif ("owo" in ctx.content) or ("uwu" in ctx.content):
            
            for name in self.bot.t.command_names:
                
                if ctx.content.startswith(f"owo{name}"):
                    return

                if ctx.content.startswith(f"uwu{name}"):
                    return
                    
            if ctx.author.id not in self.owo_cache:
                
                self.owo_cache.append(ctx.author.id)
                await self.bot.hdb.add_count(ctx.author.id, "owo")

                await asyncio.sleep(10)

                self.owo_cache.remove(ctx.author.id)

        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if self.bot.d.verification_msg_id == payload.message_id:
            
            channel = self.bot.get_channel(payload.channel_id)
            await channel.send("verified")

            member = self.bot.d.bhv.get_member(payload.user_id)
            await member.add_roles(*self.bot.d.verify_roles)

    async def handle_command_cooldown(self, ctx, remaining):
        await ctx.channel.send(f"This command is on cooldown, please wait another **{round(remaining, 2)}s** to use it again!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        print(e)
        if isinstance(e, commands.CommandOnCooldown):
            await self.handle_command_cooldown(ctx, e.retry_after)

        elif isinstance(e, commands.MissingRequiredArgument):
            await ctx.channel.send(self.bot.t.errors.missing_arg.format(self.bot.t.command_help_str[ctx.command]["syntax"]))

        elif isinstance(e, BAD_ARG_ERRORS):
            await ctx.channel.send(self.bot.t.errors.bad_arg)

        elif isinstance(e, IGNORED_ERRORS):
            return

        else:
            await ctx.channel.send(f"Oops, it seems that an error occurred.")
            raise e


async def setup(bot):
    await bot.add_cog(Events(bot))