import discord
from numpy import random
import requests
from discord import app_commands
from discord.ext import commands
from CBot import DClient as CBotDClient
from Customs.Navigators import ButtonNavigator as Navigator

class Nasa(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    @app_commands.command(name="apod", description="A Daily Astronomy Post by NASA.")
    @app_commands.checks.cooldown(1, 1)
    async def GetNasaApod(self, ctx:discord.Interaction) -> None:
        NASAapod = requests.get("https://api.nasa.gov/planetary/apod?api_key=0dsw3SiQmYCeNnwKZROSQIyrcZqjoDzMBo4ggCwS", headers={"Accept": "application/json"}).json()
        Explanation = NASAapod["explanation"][:1021]
        DEm = discord.Embed(title=NASAapod["title"], description=f'Date {NASAapod["date"]}', color=0xA9775A)
        DEm.add_field(name="Explanation:", value=Explanation, inline=False)
        if "hdurl" in NASAapod: DEm.set_image(url=NASAapod["hdurl"])
        else: DEm.add_field(name="\u200b", value=f'[Video Url]({NASAapod["url"]})', inline=False)
        if "copyright" in NASAapod: DEm.set_footer(text=f'Copyright: {NASAapod["copyright"]}')
        await ctx.response.send_message(embed=DEm)

    # @app_commands.command(name="mars", description="Images From Mars.")
    # @app_commands.checks.cooldown(1, 1)
    # async def GetNasaMars(self, ctx:discord.Interaction) -> None:
    #     def MakeEmbed(MarsImage, ImageNum, Total) -> discord.Embed:
    #         NEm = discord.Embed(title="Mars", description="By: Curiosity Rover (NASA)", color=0xCD5D2E)
    #         NEm.set_thumbnail(url="https://i.imgur.com/xmSmG0f.jpeg")
    #         NEm.add_field(name="Camera:", value=MarsImage["camera"]["full_name"], inline=True)
    #         NEm.add_field(name="Taken on:", value=MarsImage["earth_date"], inline=True)
    #         NEm.add_field(name=f"`Image: {ImageNum+1}/{Total}`", value="\u200b", inline=False)
    #         NEm.set_image(url=MarsImage["img_src"])
    #         return NEm
    #     NASAmars = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=0dsw3SiQmYCeNnwKZROSQIyrcZqjoDzMBo4ggCwS", 
    #                             headers={"Accept": "application/json"}).json()
    #     MarsImages = random.sample(NASAmars["photos"], k=25)
    #     Images = [MakeEmbed(i, v, len(MarsImages)) for v, i in enumerate(MarsImages)]
    #     await Navigator(ctx, Images).autoRun()

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")

async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(Nasa(DClient))