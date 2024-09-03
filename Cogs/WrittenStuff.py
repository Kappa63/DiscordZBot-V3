import discord
from discord import app_commands
from discord.ext import commands
import requests
import randfacts
from CBot import DClient as CBotDClient
from Setup import NClient
from Customs.Functions import SendWait
import re


class WrittenStuff(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    @app_commands.command(name="advice", description="Because a Discord Bot is Where you Should be Getting Advice From.")
    @app_commands.checks.cooldown(1, 1)
    async def RandomAdvice(self, ctx:discord.Interaction) -> None:
        Advice = requests.get("https://api.adviceslip.com/advice", headers={"Accept": "application/json"} ).json()
        await ctx.response.send_message(embed=discord.Embed(title="Some Advice", description=Advice["slip"]["advice"], color=0x7DD7D8))
    
    @app_commands.command(name="news", description="Latest Headline News.")
    @app_commands.checks.cooldown(1, 3)
    async def TheNews(self, ctx:discord.Interaction) -> None:
        News = requests.get("https://newsapi.org/v2/top-headlines", params=NClient).json()
        NEm = discord.Embed(title = "News", color = 0x0F49B2)
        for Num, Article in enumerate(News["articles"], start=1): 
            NEm.add_field(name = f'`{Num}.` {Article["title"]}. **Published On:** {re.sub("T", " ", Article["publishedAt"])[:-1]}', value=Article["url"])
        await ctx.response.send_message(embed = NEm)

    @app_commands.command(name="fact", description="Did you Know this Command Sends Fun Facts?")
    @app_commands.checks.cooldown(1, 1)
    async def GetAFact(self, ctx:discord.Interaction): await ctx.response.send_message(embed=discord.Embed(title="Fact", description=randfacts.getFact(), color=0x1F002A))

    
    BinarySlashes = app_commands.Group(name="binary", description="Main Command Group for Binary.")
   
    @BinarySlashes.command(name="create", description="Text to Binary.")
    @app_commands.rename(txt="text")
    @app_commands.describe(txt="Text to Convert to Binary")
    @app_commands.checks.cooldown(1, 1)
    async def To(self, ctx:discord.Interaction, txt:str) -> None:
        Binary = " ".join([format(i,"b") for i in bytearray(txt,"utf-8")])
        await ctx.response.send_message(embed = discord.Embed(title = "Convert To Binary", description = Binary[:2048], color = 0x5ADF44))

    @BinarySlashes.command(name="read", description="Binary to Text")
    @app_commands.rename(bin="binary")
    @app_commands.describe(bin="Text to Convert to Binary")
    @app_commands.checks.cooldown(1, 1)
    async def From(self, ctx:discord.Interaction, bin:str) -> None:
        try:
            String = "".join([chr(int(Binary, 2)) for Binary in bin.split(" ")])
            try:
                requests.get(String)
                await ctx.response.send_message(String)
            except: await ctx.response.send_message(embed = discord.Embed(title = "Convert To Text", description = String[:2048], color = 0x5ADF44))
        except ValueError: await SendWait(ctx, "Something went wrong. Check if the binary has any errors.")

    @app_commands.command(name="kanye", description="Kanye Yaps. Here are his Yaps.")
    @app_commands.checks.cooldown(1, 1)
    async def ShitByKanye(self, ctx:discord.Interaction) -> None:
        KanyeSays = requests.get("https://api.kanye.rest", headers={"Accept": "application/json"}).json()
        await ctx.response.send_message(embed=discord.Embed(title="Kanye Says Alot, Here's One", description=KanyeSays["quote"], color=0x53099B))

    @app_commands.command(name="insult", description="Sometimes you Need to Curb your Ego,")
    @app_commands.checks.cooldown(1, 1)
    async def RandomInsult(self, ctx:discord.Interaction) -> None:
        InsultGot = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json", headers={"Accept": "application/json"}).json()
        await ctx.response.send_message(embed=discord.Embed( title="Insult", description=InsultGot["insult"], color=0xBD2DB8))

    @app_commands.command(name="dadjoke", description="Remember your Dad's Lame Jokes.")
    @app_commands.checks.cooldown(1, 1)
    async def KillMe(self, ctx:discord.Interaction) -> None:
        DadJoke = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"}).json()
        await ctx.response.send_message(embed=discord.Embed(title="Dad Joke", description=DadJoke["joke"], color=0x99807E))

    @app_commands.command(name="joke", description="Jokes for a Tamer Audience.")
    @app_commands.checks.cooldown(1, 1)
    async def Joke(self, ctx:discord.Interaction) -> None:
        Joke = requests.get("https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit", #?blacklistFlags=
                            headers={"Accept": "application/json"}).json()
        if Joke["type"] == "twopart": 
            await ctx.response.send_message(embed=discord.Embed(title=f'Joke ({Joke["category"]})', description=f'{Joke["setup"]}\n\n||{Joke["delivery"]}||', color=0xEB88DA))
        else: await ctx.response.send_message(embed=discord.Embed(title=f'Joke ({Joke["category"]})', description=Joke["joke"], color=0xEB88DA))

    @app_commands.command(name="darkjoke", description="A Joke so Dark it will Probably Make you Uncomfortable.")
    @app_commands.checks.cooldown(1, 1)
    async def DarkJoke(self, ctx:discord.Interaction) -> None:
        DarkJoke = requests.get("https://sv443.net/jokeapi/v2/joke/Dark", headers={"Accept": "application/json"}).json()
        if DarkJoke["type"] == "twopart": 
            await ctx.response.send_message(embed=discord.Embed(title=f'Joke ({DarkJoke["category"]})', description=f'{DarkJoke["setup"]}\n\n||{DarkJoke["delivery"]}||',
                                                               color=0xD8DCCD))
        else: await ctx.response.send_message(embed=discord.Embed(title=f'Joke ({DarkJoke["category"]})', description=DarkJoke["joke"], color=0xD8DCCD))

    @app_commands.command(name="pun", description="Ba Dumm Tiss.")
    @app_commands.checks.cooldown(1, 1)
    async def Pun(self, ctx:discord.Interaction) -> None:
        Pun = requests.get("https://sv443.net/jokeapi/v2/joke/Pun", headers={"Accept": "application/json"}).json()
        if Pun["type"] == "twopart": await ctx.response.send_message(embed=discord.Embed(title="Pun", description=f'{Pun["setup"]}\n\n||{Pun["delivery"]}||', color=0x05D111))
        else: await ctx.response.send_message(embed=discord.Embed(title="Pun", description=Pun["joke"], color=0x05D111))

    @app_commands.command(name="qotd", description="A Daily Quote.")
    @app_commands.checks.cooldown(1, 1)
    async def QuoteOfTheDay(self, ctx:discord.Interaction) -> None:
        TodayQuote = requests.get(
            "https://favqs.com/api/qotd", headers={"Accept": "application/json"}
        ).json()
        QEm = discord.Embed(
            title="Quote Of The Day",
            description=TodayQuote["quote"]["body"],
            color=0x8D42EE,
        )
        QEm.set_footer(text=f'By: {TodayQuote["quote"]["author"]}')
        await ctx.response.send_message(embed=QEm)

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")

async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(WrittenStuff(DClient))