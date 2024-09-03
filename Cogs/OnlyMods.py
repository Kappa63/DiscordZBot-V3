import discord
from discord import app_commands
from discord.ext import commands
from Customs.Functions import ChDev, RefreshMAL
from Setup import Eco
from CBot import DClient as CBotDClient
from typing import Optional

class OnlyMods(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    @app_commands.command(name="status", description="Revealse the Current Status of ZBot.")
    @app_commands.checks.cooldown(1, 1)
    async def BotStatus(self, ctx:discord.Interaction) -> None:
        SEm = discord.Embed(title="<:bnr0:1230869635826450462><:bnr1:1230869697893761106><:bnr2:1230869719905603615><:bnr3:1230869735554682910><:bnr4:1230869757146828831>", color=0x000000)
        SEm.add_field(name="Guilds in: ", value=len(self.DClient.guilds), inline=False)
        SEm.add_field(name="Latency: ", value=self.DClient.latency * 100, inline=False)
        SEm.add_field(name="ShardCount: ", value=self.DClient.shard_count, inline=False)
        SEm.add_field(name="Loaded Cogs: ", value="\n".join(self.DClient.LoadedCogs), inline=False)
        await ctx.response.send_message(embed=SEm)

    @commands.command(name="sync")
    @commands.check(ChDev)
    async def Syncer(self, ctx:commands.Context) -> None:
        try:
            slashSync = await self.DClient.tree.sync()
            await ctx.send(embed=discord.Embed(title=f"Synced {len(slashSync)} command(s)"))
        except Exception as e:
            print(e)

    @commands.command(name="balset")
    @commands.check(ChDev)
    async def ecoBalSetter(self, ctx:commands.Context, n:float, id:int=None) -> None:
        Dt = Eco.update_one({"_id":id if id else ctx.author.id}, {"$set": {"bal":n}})
        await ctx.send(embed=discord.Embed(title=f"{'User' if id else 'Your'} Balance is ${n}" if Dt.modified_count else "Failed to Set"))

    @commands.command(name="achpush")
    @commands.check(ChDev)
    async def ecoAchSetter(self, ctx:commands.Context, n:int, s:bool, id:int=None) -> None:
        Dt = Eco.update_one({"_id":id if id else ctx.author.id}, {"$push": {"achieved":[n, s]}})
        await ctx.send(embed=discord.Embed(title=f"Achievement ID {n} Added to {'User' if id else 'You'}" if Dt.modified_count else "Failed to Add"))

    @app_commands.command(name="embed", description="Creates an embed")
    @app_commands.rename(t="title")
    @app_commands.describe(t="Title of the Embed")
    @app_commands.rename(d="description")
    @app_commands.describe(d="Description Text of the Embed")
    @app_commands.rename(c="color")
    @app_commands.describe(c="Embed's Bar Color in HEX")
    @app_commands.rename(i="image")
    @app_commands.describe(i="Embed Image")
    @app_commands.checks.cooldown(1, 1)
    async def slash_Embedder(self, ctx:discord.Interaction, t:str, d:str, c:str, i:Optional[discord.Attachment]=None) -> None:
        sEm = discord.Embed(title=t, description=d, color=int(c, 16))
        if i: sEm.set_image(url=i.url)
        await ctx.response.send_message(embed=sEm)

    @commands.command(name="reloadall")
    @commands.check(ChDev)
    async def MassCogReloader(self, ctx:commands.Context) -> None:
        await self.DClient.reload_all_cogs()
        REm = discord.Embed(title="ZBot Reloaded", color = 0x000000)
        REm.add_field(name="Cogs Reloaded: ", value="\n".join(self.DClient.LoadedCogs), inline=False)
        await ctx.send(embed=REm)

    @commands.command(name="reload")
    @commands.check(ChDev)
    async def CogReloader(self, ctx:commands.Context, *args) -> None:
        await self.DClient.reload_cogs(args)
        REm = discord.Embed(title="ZBot Reloaded", color = 0x000000)
        REm.add_field(name="Cogs Reloaded: ", value="\n".join(args), inline=False)
        await ctx.send(embed=REm)

    @commands.command(name="unload")
    @commands.check(ChDev)
    async def CogUnloader(self, ctx:commands.Context, *args) -> None:
        await self.DClient.unload_cogs(args)
        REm = discord.Embed(title="ZBot Unloaded", color = 0x000000)
        REm.add_field(name="Cogs Unloaded: ", value="\n".join(args), inline=False)
        await ctx.send(embed=REm)
    
    @commands.command(name="load")
    @commands.check(ChDev)
    async def CogLoader(self, ctx:commands.Context, *args) -> None:
        await self.DClient.load_cogs(args)
        REm = discord.Embed(title="ZBot Loaded", color = 0x000000)
        REm.add_field(name="Cogs loaded: ", value="\n".join(args), inline=False)
        await ctx.send(embed=REm)

    # @commands.command(name="makedown")
    # @commands.check(ChDev)
    # async def MakeBotOff(self, ctx):
    #     await self.DClient.change_presence(status=discord.Status.invisible)
    #     StateFile = open("OpenState.txt", "w+")
    #     StateFile.write("Down")
    #     StateFile.close()
    #     await SendWait(ctx, "Bot Invisible (Down)")

    # @commands.command(name="makeup")
    # @commands.check(ChDev)
    # async def MakeBotOn(self, ctx):
    #     await self.DClient.change_presence(status=discord.Status.online, activity=discord.Game(f"zhelp || {random.choice(Doing)}"))
    #     StateFile = open("OpenState.txt", "w+")
    #     StateFile.write("Up")
    #     StateFile.close()
    #     await SendWait(ctx, "Bot Visible (Up)")

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")

async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(OnlyMods(DClient))