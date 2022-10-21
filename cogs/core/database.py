from discord.ext import commands
import datetime
import pytz


class Database(commands.Cog, name="Database"):

    def __init__(self, bot):
        self.bot = bot

    async def curser_to_list(self, curser):
        return [doc async for doc in curser]

    async def add_count(self, uid, type):
        
        today = datetime.date.today()
        query = {"uid": str(uid), "time": pytz.timezone("America/Los_angeles").localize(datetime.datetime(today.year, today.month, today.day))} # user pytz localize to fix time
        values = {
            "$inc": {type: 1}
        }

        await self.bot.db.count.update_one(query, values, upsert=True)

    async def get_user_count(self, uid, time): # basically every doc kek
        return await self.curser_to_list(self.bot.db.count.find({"time": {"$gte": time}, "uid": str(uid)}))

    async def get_by_time(self, time):
        return await self.curser_to_list(self.bot.db.count.find({"time": {"$gte": time}}))


async def setup(bot):
    await bot.add_cog(Database(bot))