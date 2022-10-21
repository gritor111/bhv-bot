import classyjson as cj
import os
import discord
import datetime
import pytz
from dateutil.relativedelta import relativedelta

def load_text():
    text = {}

    for filename in os.listdir("data/text"):
        with open(f"data/text/{filename}", "r", encoding="utf8") as f:
            text.update(cj.loads(f.read()))

    return cj.ClassyDict(text)

def load_data() -> cj.ClassyDict:
    with open("data/data.json", "r", encoding="utf8") as f:
        data = cj.loads(f.read())
    
    return data


def mod_data(bot):
    
    guild = bot.get_guild(bot.d.bhv)
    
    bot.d.verify_roles = [guild.get_role(role_id) for role_id in bot.d.verify_roles]
    bot.d.bhv = guild


def get_files(path, files):
    
    all_files = []
    filenames = os.listdir(path)
    
    for f in filenames:
        f_path = path + "/" + f

        if os.path.isdir(f_path):
            
            all_files.extend(get_files(f_path, all_files))

        elif f_path.endswith(".py"):
            all_files.append(f_path)

    return all_files


def get_time(time):

    tz = pytz.timezone("America/Los_angeles")
    midnight = datetime.datetime.combine(datetime.date.today(), datetime.time())

    if time in ["m", "month", "monthly"]:
        return [tz.localize(midnight - relativedelta(months=1)), "Monthly"]
        
    elif time in ["w", "weekly", "week"]:
        return [tz.localize(midnight - relativedelta(weeks=1)), "Weekly"]
        
    elif time in ["d", "daily", "day"]:
        return [tz.localize(midnight), "Daily"]

    elif time in ["All time", "at"]:
        return [tz.localize(datetime.datetime(1969, 1, 1)), "All time"]
        
   