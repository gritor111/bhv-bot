from util.setup import get_time
from discord.ext import commands
import discord


class Stats(commands.Cog, name='Stats'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats", aliases=["s"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stats(self, ctx, *, time="All time"):

        if time not in ["All time", "at", "d", "daily", "day", "w", "weekly", "week", "m", "month", "monthly"]:
            await ctx.channel.send(self.bot.t.errors.bad_arg.format(self.bot.t.command_help_str[ctx.command.name]["syntax"]))
            return

        time, time_str = get_time(time)
        user_count = await self.bot.hdb.get_user_count(ctx.author.id, time)
        embed = discord.Embed(color=discord.Colour.from_str("#f77394"))

        total_owos, total_hunts, total_battle = 0, 0, 0
        for count in user_count:
            total_owos += count["owo"]
            total_hunts += count["hunt"]
            total_battle += count["battle"]

        desc = f""":medal: **Score** - {(total_owos + total_hunts + total_battle)//3}
        
        :seedling: **Hunt** - {total_hunts}
        
        :crossed_swords: **Battles** - {total_battle}
                    
        :large_blue_diamond: **OwO** - {total_owos}"""

        embed.description = desc
        embed.set_author(name=f"{time_str} stats for {ctx.author.name}", icon_url=ctx.author.avatar.url)

        await ctx.channel.send(embed=embed)

    @commands.command(name="leaderboards", aliases=["lb", "lbs"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def leaderboards(self, ctx, type="owo", *, limit_time="10 daily"):
        try:
            limit = 10
            time = "daily"
            if limit_time.lower() in ["all time", "at", "d", "daily", "day", "w", "weekly", "week", "m", "month", "monthly"]:
                time = limit_time

            elif int(limit_time):
                limit = int(limit_time)

            else:
                limit, time = int(limit_time.split()[0]), " ".join(limit_time.split()[1:])

        except ValueError:
            await ctx.channel.send(self.bot.t.errors.bad_arg.format(self.bot.t.command_help_str[ctx.command.name]["syntax"]))
            return
        print(time, limit)
        if (type.lower() not in ["owo", "hunt", "battle"]) or time.lower() not in ["all time", "at", "d", "daily", "day", "w", "weekly", "week", "m", "month", "monthly"]:
            await ctx.channel.send(self.bot.t.errors.bad_arg.format(self.bot.t.command_help_str[ctx.command.name]["syntax"]))
            return

        if limit > 25:
            await self.bot.util.send(ctx, self.bot.t.lb.big_limit)
            return

        time = get_time(time)
        users = await self.bot.hdb.get_by_time(time[0])
        lb = self.craft_lb(users, type, limit)
        embed = self.bot.embed
        embed.title = f"{time[1].capitalize()} {type}s leaderboard"
        embed.description = lb

        await ctx.channel.send(embed=embed)

    def craft_lb(self, users, type, limit):
        users_dict = {}

        for doc in users:
            if doc["uid"] not in doc:
                users_dict[doc["uid"]] = {"owo": doc["owo"], "hunt": doc["hunt"], "battle": doc["battle"]}
                continue

            users_dict[doc["uid"]]["owo"] += doc.owo
            users_dict[doc["uid"]]["hunt"] += doc.hunt
            users_dict[doc["uid"]]["battle"] += doc.battle

        users_dict = dict(sorted(users_dict.items(), key=lambda doc: doc[1][type], reverse=True))

        desc = ""

        for i, user in enumerate(list(users_dict.items())[:limit]):
            member = self.bot.get_user(int(user[0]))
            desc += f"#{i + 1} `{user[1][type]}` - **{member.name}**\n"

        return desc


async def setup(bot):
    await bot.add_cog(Stats(bot))
