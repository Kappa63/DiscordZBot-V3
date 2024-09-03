import discord
from discord.ext import commands
from discord import app_commands
from Setup import IMClient
from Customs.Functions import SendWait
from CBot import DClient as CBotDClient
from Customs.UI.Selector import SelectionView as Selector


def MvEmbed(IMDbinfo) -> discord.Embed:
    PlotF = None
    if "plot outline" in IMDbinfo: PlotF = IMDbinfo["plot outline"][:100]

    YEm = discord.Embed(title=IMDbinfo["original title"], description=", ".join(IMDbinfo["genres"]), url=f'https://www.imdb.com/title/tt{IMDbinfo["imdbID"]}', 
                        color=0xDBA506)
    if PlotF: YEm.add_field(name="Plot:", value=PlotF + "\n", inline=False)
    if "original air date" in IMDbinfo: YEm.add_field(name="Original Air Date:", value=IMDbinfo["original air date"], inline=False)
    if "box office" in IMDbinfo:
        Box = ""
        if "Budget" in IMDbinfo["box office"]: Box += f'Budget: {IMDbinfo["box office"]["Budget"].split(" ")[0]}'
        if "Opening Weekend United States" in IMDbinfo["box office"]: Box += f'\nOpening Week: {IMDbinfo["box office"]["Opening Weekend United States"].split(" ")[0]}'
        if "Cumulative Worldwide Gross" in IMDbinfo["box office"]: Box += f'\nTotal Gross: {IMDbinfo["box office"]["Cumulative Worldwide Gross"].split(" ")[0]}'
        if Box: YEm.add_field(name="Box Office:", value=Box, inline=True)
    if "number of seasons" in IMDbinfo: YEm.add_field(name="Seasons:", value=IMDbinfo["number of seasons"], inline=True)
    if "rating" in IMDbinfo: YEm.add_field(name="Rating:", value=IMDbinfo["rating"], inline=True)
    if "cast" in IMDbinfo:
        Cast = [Member["name"] for Member in IMDbinfo["cast"][:10]]
        Note = "\n**And more...**" if len(IMDbinfo["cast"]) > 10 else ""
        YEm.add_field(name="Cast:", value="\n".join(Cast[:10]) + Note, inline=False)
    if "cover url" in IMDbinfo: YEm.set_thumbnail(url=IMDbinfo["cover url"])
    return YEm

class Movies(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    IMDbSlashes = app_commands.Group(name="imdb", description="Main Command Group for IMDb.")

    @IMDbSlashes.command(name="get", description="Find Info About Your Favourite Movie.")
    @app_commands.rename(mv="movie")
    @app_commands.describe(mv="Movie Name to Find")
    @app_commands.checks.cooldown(1, 3)
    async def MovieGetter(self, ctx:discord.Interaction, mv:str) -> None:
        if not mv: await SendWait(ctx, "No Arguments :no_mouth:"); return
        
        await ctx.response.defer(thinking=True)
        try:
            IMDbtempID = IMClient.search_movie(mv, results=1)[0].movieID
            IMDbI = IMClient.get_movie(IMDbtempID).data
        except IndexError: await SendWait(ctx, "Nothing Found :woozy_face:"); return
        await ctx.followup.send(embed=MvEmbed(IMDbI))

    @IMDbSlashes.command(name="search", description="Search for Your Favourite Movie.")
    @app_commands.rename(mv="movie")
    @app_commands.describe(mv="Movie Name to Find")
    @app_commands.checks.cooldown(1, 3)
    async def MovieSrchr(self, ctx:discord.Interaction, mv:str) -> None:
        async def exTimOt():
            await ctx.edit_original_response(embed=discord.Embed(title=":x: Search Timeout or Cancelled", color=0x3695BA), view=None)

        async def getSel(id):
            IMDbChoice = SrchIMDb[int(id) - 1]
            IMDbID = IMDbChoice.movieID
            Md = ""
            if "kind" in IMDbChoice.data: Mk = IMDbChoice.data["kind"]
            My = ""
            if "year" in IMDbChoice.data: My = IMDbChoice.data["year"]
            await ctx.edit_original_response(embed=discord.Embed(title=":calling: Finding...", 
                                                    description=f'{IMDbChoice.data["title"]} ({Mk}) ({My})',
                                                    color=0xDBA506), view=None)
            IMDbI = IMClient.get_movie(IMDbID).data
            await ctx.edit_original_response(embed=MvEmbed(IMDbI))

        if not mv: await SendWait(ctx, "No Arguments :no_mouth:"); return
        await ctx.response.defer(thinking=True)
        C = 0
        SrchIMDb = []
        for Movie in IMClient.search_movie(mv, results=10):
            C += 1
            if C == 1: SYem = discord.Embed(title=f':mag: Search for "{mv}"', description="\u200b", color=0xDBA506)
            Md = ""
            if "kind" in Movie.data: Mk = Movie.data["kind"]
            My = ""
            if "year" in Movie.data: My = Movie.data["year"]
            SYem.add_field(name="\u200b", value=f'{C}. `{Movie.data["title"]} ({Mk}) ({My})`', inline=False)
            SrchIMDb.append(Movie)
        if not C: await SendWait(ctx, "Nothing Found :woozy_face:"); return
        SYem.set_footer(text='Choose a number to check Movie or Series. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
        await ctx.followup.send(embed=SYem, view=Selector(getSel, exTimOt, list(range(1, C+1))))

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")

async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(Movies(DClient))