from discord.ext import commands
import discord
from CBot import DClient as CBotDClient
from discord import app_commands
from Customs.Functions import SendWait, FormatTime, Ignore, IsBot, IsNSFW, IsAdmin
from numpy import random

Doing = ["ZBot IS BACK ONLINE!!", "4 Years Later", "Revived from the Dead"]

class MainEvents(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient
        
    @commands.Cog.listener("on_ready")
    async def on_ready(self) -> None:
        await self.DClient.change_presence(activity=discord.Game(f"{random.choice(Doing)}"))
        print(f"Online in {len(self.DClient.guilds)}...")
        self.DClient.StaffChannel = self.DClient.get_channel(768461226996662302)
        self.DClient.Me = self.DClient.get_user(443986051371892746)
        self.DClient.tree.error(self.on_app_command_error)
        
        await self.DClient.StaffChannel.send(f"Back Online In {len(self.DClient.guilds)}...")

    async def on_app_command_error(self, ctx:discord.Interaction, error) -> None:
        await ctx.response.defer()
        if isinstance(error, app_commands.CommandOnCooldown): await SendWait(ctx, f'Hold the spam. Wait atleast {FormatTime(round(error.retry_after, 2))}')
        elif isinstance(error, IsAdmin): await SendWait(ctx, "Non-admins are not allowed to use this command")
        # elif isinstance(error, IsVote): await ctx.send(embed=ErrorEmbeds("Vote"))
        # elif isinstance(error, IsPatreon): await ctx.send(embed=ErrorEmbeds("Patreon"))
        # elif isinstance(error, IsPatreonT2): await ctx.send(embed=ErrorEmbeds("PatreonT2"))
        # elif isinstance(error, IsPatreonT3): await ctx.send(embed=ErrorEmbeds("PatreonT3"))
        # elif isinstance(error, IsPatreonT4): await ctx.send(embed=ErrorEmbeds("PatreonT4"))
        # elif isinstance(error, IsSetup): await SendWait(ctx, 'Please setup your server first (with "zsetup")! Check all server commands (with "zhelp server")')
        elif isinstance(error, IsNSFW): await SendWait(ctx, "This can only be used in NSFW channels.")
        # elif isinstance(error, IsMultiredditLimit): await SendWait(ctx, "You can no longer have this many Multireddits. Remove some to comply with your limit. Until then you cannot use your Multireddits.")
        elif isinstance(error, (app_commands.CommandNotFound, Ignore, IsBot)):print(error); return
        else:
            print(error)
            await self.DClient.StaffChannel.send(self.DClient.Me.mention)
            await self.DClient.StaffChannel.send(f'In {ctx.command}: {error}')
            return

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")
    

async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(MainEvents(DClient))