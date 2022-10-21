import discord
from discord.ext import commands
from util.setup import load_text

class HelpCommand(commands.HelpCommand):

    def __init__(self, bot):
        self.bot = bot
        self.bot.t = load_text()
        super().__init__()

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Bot help", color=discord.Colour.from_str("#f77394"), description=self.bot.t.command_help_str.help.desc)
        # `mapping` is a dict of the bot's cogs, which map to their commands
        mapping = dict(filter(lambda item: (len(item[1]) > 0) and item[0], mapping.items()))
        print(mapping)
        for cog, cmds in mapping.items():  # get the cog and its commands separately
            if cog.qualified_name == "Developer Commands":
                continue

            embed.add_field(
                name=cog.qualified_name,  # get the cog name
                value=" ".join(["`" + cmd.name + "`" for cmd in cmds]),
                inline=False
            )

        channel = self.get_destination()  # this method is inherited from `HelpCommand`, and gets the channel in context
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        if command.hidden:
            return

        embed = discord.Embed(title="Command help", color=discord.Colour.from_str("#f77394"))
        help_strings = self.bot.t.command_help_str[command.name]

        embed.add_field(name="Syntax:", value=f'`{help_strings["syntax"]}`', inline=False)
        embed.add_field(name="Description:", value=help_strings["desc"], inline=False)
        embed.add_field(name="Aliases:", value=", ".join(command.aliases), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)


