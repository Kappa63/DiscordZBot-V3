import discord
from discord import app_commands
from discord.ext import commands
from numpy import random
import cv2
import numpy as np
from CBot import DClient as CBotDClient
import os
from Setup import GClient, GApi
from Customs.Functions import SendWait


class Randomizers(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    @app_commands.command(name="roll", description="Roll a Dice.")
    @app_commands.checks.cooldown(2, 1)
    async def RollTheDice(self, ctx:discord.Interaction) -> None:
        DiceFaces = {1: "https://i.imgur.com/hHO0UrI.png", 2: "https://i.imgur.com/pg5M3TR.png",
                     3: "https://i.imgur.com/ToNk0YB.png", 4: "https://i.imgur.com/QvcZzRQ.png",
                     5: "https://i.imgur.com/6LkxfKL.png", 6: "https://i.imgur.com/vBRUNQO.png"}
        DiceRolls = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
        FaceNumber = random.randint(1, 6)
        DEm = discord.Embed(title="Dice Roll", description=f"**The Dice Rolled a:** *{FaceNumber} ({DiceRolls[FaceNumber]})*", color=0xFAC62D)
        DEm.set_thumbnail(url=DiceFaces[FaceNumber])
        await ctx.response.send_message(embed=DEm)

    @app_commands.command(name = "coinflip", description="Flip a Coin.")
    @app_commands.checks.cooldown(2, 1)
    async def FlipTheCoin(self, ctx:discord.Interaction) -> None:
        CoinFaces = {"Heads": "https://i.imgur.com/U6BxOan.png",
                     "Tails": "https://i.imgur.com/zWvC1Ao.png"}
        Face = random.choice(list(CoinFaces.keys()))
        CEm = discord.Embed(title="Coin Flip", description=f"**The Coin Landed on:** *{Face}*", color=0xFAC62D)
        CEm.set_thumbnail(url=CoinFaces[Face])
        await ctx.response.send_message(embed=CEm)

    @app_commands.command(name="color", description="Generates a Random Color.")
    @app_commands.checks.cooldown(1, 1)
    async def ColorRandom(self, ctx:discord.Interaction) -> None:
        MakeClear = np.zeros((360, 360, 3), np.uint8)
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
        MakeClear[:, 0:360] = (B, G, R)
        RGBtoHEX = "%02x%02x%02x" % (R, G, B)
        cv2.imwrite("Color.png", MakeClear)
        ClrImg = discord.File("Color.png")
        ColorObject = discord.Color(value=int(RGBtoHEX, 16))
        CEm = discord.Embed(title="Color", description=f"```-Hex: #{RGBtoHEX}\n-RGB: ({R},{G},{B})```", color=ColorObject)
        CEm.set_thumbnail(url="attachment://Color.png")
        await ctx.response.send_message(file=ClrImg, embed=CEm)
        os.remove("Color.png")

    @app_commands.command(name="giphy", description="A Random GIF Based on Search Term")
    @app_commands.rename(srch="search")
    @app_commands.describe(srch="Gif Search Term")
    @app_commands.checks.cooldown(1, 1)
    async def RandomGif(self, ctx:discord.Interaction, *, srch:str=None) -> None:
        if not srch: await SendWait(ctx, "No search term given :confused:"); return
        try:
            GifF = GApi.search_gifs(srch, api_key=GClient, serialize=True, limit=50).data
            await ctx.response.send_message(random.choice(GifF).url)
        except: await SendWait(ctx, "No gifs found :expressionless:")

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")


async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(Randomizers(DClient))