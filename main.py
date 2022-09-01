import os
from discord.ext import commands, tasks
import motor.motor_asyncio
from util.setup import load_text, load_data, mod_data, get_files
import discord
import itertools

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents=discord.Intents.all()
)
STATUS = itertools.cycle(["a", "b"])
CONNECT_STRING = os.environ.get("MONGO_SECRET")
mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://gritor111:lironfrid19@cluster0.smx4w.mongodb.net/?retryWrites=true&w=majority")
bot.db = mongo_client.bhv
bot.author_id = 656373241144934420  # Change to your discord id!!!
@bot.event 
async def on_ready():  # When the bot is ready
    for extension in files:
        print(extension)
        await bot.load_extension(extension)  # Loades every extension.
    mod_data(bot)
    change_status.start()
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(STATUS)))

files = [file.replace("/", ".")[:-3] for file in get_files("cogs", [])]

bot.t = load_text()
bot.d = load_data()
bot.hdb = bot.get_cog("Database")
token = "MTAwMDMzODU5NjAzNDc3NzA5OQ.GfG0Jz.ZB8RR6LHmt7mjYTF24_wGVHX0KiCuMv9umZdVQ"
bot.run(token)  # Starts the bot
# test commit