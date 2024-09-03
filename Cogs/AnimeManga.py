import discord
from discord.ext import commands
# import mal
from discord import app_commands
from Setup import MClient, MALsearch
from Customs.Functions import SendWait, RefreshMAL
# from Customs.Navigators import ButtonNavigator as Navigator
from Customs.UI.Selector import SelectionView as Selector
from CBot import DClient as CBotDClient

class AnimeManga(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient
    
    @app_commands.command(name="manga", description="Retrieves a Manga from MAL.")
    @app_commands.describe(manga="Manga Name")
    @app_commands.check(RefreshMAL)
    @app_commands.checks.cooldown(1, 3)
    async def MangaInfo(self, ctx:discord.Interaction, manga:str) -> None:
        async def exTimOt():
            await ctx.edit_original_response(embed=discord.Embed(title=":x: Search Timeout or Cancelled", color=0x3695BA), view=None)

        async def getSel(id):
            MangaF = SrchManga[int(id)-1]
            await ctx.edit_original_response(embed=discord.Embed(title=":calling: Finding...", description=f"{MangaF.title} **({MangaF.media_type.value})**", color=0x3695BA), view=None)
            MangaGet = MClient.get_manga_details(MangaF.id)
            # MangaGetmal = mal.Manga(MangaID)
            MangaGenres = []
            for Genre in MangaGet.genres: MangaGenres.append(Genre.name)
            altEn = MangaGet.alternative_titles.get("en")
            altJa = MangaGet.alternative_titles.get("ja")
            AEm = discord.Embed(title=f"{MangaGet.title}  /  {altEn if altEn else ''}  /  {altJa if altJa else ''} **({MangaGet.media_type.value})**", 
                                description=f'{", ".join(MangaGenres)}\n[Mal Page](https://myanimelist.net/manga/{MangaGet.id})', color=0x3695BA)
            AEm.set_thumbnail(url=MangaGet.main_picture.large)

            MangaSynopsis = MangaGet.synopsis[:1021]

            AEm.add_field(name=f'By: {", ".join([i.node.first_name+" "+i.node.last_name for i in MangaGet.authors])}', value="\u200b", inline=False)
            AEm.add_field(name="Synopsis:", value=MangaSynopsis, inline=False)
            if hasattr(MangaGet, "start_date"): AEm.add_field(name="Start Airing on:", value=MangaGet.start_date, inline=True)
            if hasattr(MangaGet, "end_date"): AEm.add_field(name="Finish Airing on:", value=MangaGet.end_date, inline=True)
            AEm.add_field(name="Status:", value=MangaGet.status.value, inline=True)
            AEm.add_field(name="Score:", value=MangaGet.mean, inline=True)
            AEm.add_field(name="Rank:", value=MangaGet.rank, inline=True)
            AEm.add_field(name="Popularity:", value=MangaGet.popularity, inline=True)
            AEm.add_field(name="No# Volumes:", value=MangaGet.num_volumes, inline=True)
            AEm.add_field(name="No# Chapters:", value=MangaGet.num_chapters, inline=True)
            MangaAdaptation = []
            MangaAlternate = []
            MangaSummary = []
            MangaSequel = []
            MangaSide = []
            MangaSpin = []
            for TMagAdp in MangaGet.related_manga:
                if TMagAdp.relation_type_formatted == "Adaptation": MangaAdaptation.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Summary": MangaSummary.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Sequel": MangaSequel.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Spin-off": MangaSpin.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Alternative version": MangaAlternate.append(TMagAdp.node.title)
                elif TMagAdp.relation_type_formatted == "Side story": MangaSide.append(TMagAdp.node.title)

            MangaSequelC = "\n".join(MangaSequel)[:950]
            MangaAdaptationC = "\n".join(MangaAdaptation)[:950]
            MangaSummaryC = "\n".join(MangaSummary)[:950]
            MangaAlternateC = "\n".join(MangaAlternate)[:950]
            MangaSpinC = "\n".join(MangaSpin)[:950]
            MangaSideC = "\n".join(MangaSide)[:950]

            if MangaSequelC or MangaAlternateC or MangaAdaptationC or MangaSideC or MangaSummaryC or MangaSpinC: AEm.add_field(name="\u200b", value="\u200b", inline=False)
            if MangaSequelC: AEm.add_field(name="Sequel:", value=MangaSequelC, inline=False)
            if MangaAlternateC: AEm.add_field(name="Alternate Version:", value=MangaAlternateC, inline=False)
            if MangaAdaptationC: AEm.add_field(name="Adaptation:", value=MangaAdaptationC, inline=False)
            if MangaSideC: AEm.add_field(name="Side Story:", value=MangaSideC, inline=False)
            if MangaSummaryC: AEm.add_field(name="Summary:", value=MangaSummaryC, inline=False)
            if MangaSpinC: AEm.add_field(name="Spin Off:", value=MangaSpinC, inline=False)
            await ctx.edit_original_response(embed=AEm)
        
        if not manga: await SendWait(ctx, "No Arguments :no_mouth:"); return
        MangaInput = manga
        C = 0
        SrchManga = []
        await ctx.response.send_message(embed=discord.Embed(title=":mag: Searching...", color=0x3695BA))
        SAEm = discord.Embed(title=f":mag: Results for '{MangaInput}'", color=0x3695BA)
        for MangaResult in MClient.search_manga(MangaInput, limit=10, fields=MALsearch):
            C += 1
            SAEm.add_field(name="\u200b", value=f"{C}. `{MangaResult.title}` **({MangaResult.media_type.value})**", inline=False)
            SrchManga.append(MangaResult)
        await ctx.edit_original_response(embed=SAEm, view=Selector(getSel, exTimOt, list(range(1, C+1))))

    @app_commands.command(name="anime", description="Retrieves a Anime from MAL.")
    @app_commands.describe(anime="Anime Name")
    @app_commands.check(RefreshMAL)
    @app_commands.checks.cooldown(1, 3)
    async def AnimeInfo(self, ctx:discord.Interaction, anime:str) -> None:
        async def exTimOt():
            await ctx.edit_original_response(embed=discord.Embed(title=":x: Search Timeout or Cancelled", color=0x3695BA), view=None)

        async def getSel(id):
            AnimeF = SrchAnime[int(id)-1]
            await ctx.edit_original_response(embed=discord.Embed(title=":calling: Finding...", 
                                                            description=f"{AnimeF.title}", color=0x3FC0FF), view=None)
            AnimeGet = MClient.get_anime_details(AnimeF.id)
            AnimeGenres = []
            for Genre in AnimeGet.genres: AnimeGenres.append(Genre.name)
            altEn = AnimeGet.alternative_titles.get("en")
            altJa = AnimeGet.alternative_titles.get("ja")
            AEm = discord.Embed(title=f"{AnimeGet.title}  /  {altEn if altEn else ''}  /  {altJa if altJa else ''} **({AnimeGet.media_type.value})**", 
                                description=f'{", ".join(AnimeGenres)}\n[Mal Page](https://myanimelist.net/anime/{AnimeGet.id})', color=0x3FC0FF)
            AEm.set_thumbnail(url=AnimeGet.main_picture.large)
            AnimeSynopsis = AnimeGet.synopsis[:1021]
            AEm.add_field(name=f'Studios: {", ".join([i.name for i in AnimeGet.studios])}', value="\u200b", inline=False)
            AEm.add_field(name="Synopsis:", value=AnimeSynopsis, inline=False)
            if hasattr(AnimeGet, "start_date"): AEm.add_field(name="Start Airing on:", value=AnimeGet.start_date, inline=True)
            if hasattr(AnimeGet, "end_date"): AEm.add_field(name="Finish Airing on:", value=AnimeGet.end_date, inline=True)
            AEm.add_field(name="Status:", value=AnimeGet.status, inline=True)
            AEm.add_field(name="Rating:", value=AnimeGet.rating, inline=False)
            AEm.add_field(name="Score:", value=AnimeGet.mean, inline=True)
            AEm.add_field(name="Rank:", value=AnimeGet.rank, inline=True)
            AEm.add_field(name="Popularity:", value=AnimeGet.popularity, inline=True)
            AEm.add_field(name="No# Episodes:", value=AnimeGet.num_episodes, inline=True)
            AEm.add_field(name="Episode Duration:", value=int(AnimeGet.average_episode_duration/60), inline=True)
            AnimeAdaptation = []
            AnimeAlternate = []
            AnimeSummary = []
            AnimeSequel = []
            AnimeSide = []
            AnimeSpin = []
            for TAniAdp in AnimeGet.related_anime:
                if TAniAdp.relation_type_formatted == "Adaptation": AnimeAdaptation.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Summary": AnimeSummary.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Sequel": AnimeSequel.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Spin-off": AnimeSpin.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Alternative version": AnimeAlternate.append(TAniAdp.node.title)
                elif TAniAdp.relation_type_formatted == "Side story": AnimeSide.append(TAniAdp.node.title)

            AnimeSequelC = "\n".join(AnimeSequel)[:950]
            AnimeAdaptationC = "\n".join(AnimeAdaptation)[:950]
            AnimeSummaryC = "\n".join(AnimeSummary)[:950]
            AnimeAlternateC = "\n".join(AnimeAlternate)[:950]
            AnimeSpinC = "\n".join(AnimeSpin)[:950]
            AnimeSideC = "\n".join(AnimeSide)[:950]

            if AnimeSequelC or AnimeAlternateC or AnimeAdaptationC or AnimeSideC or AnimeSummaryC or AnimeSpinC: AEm.add_field(name="\u200b", value="\u200b", inline=False)
            if AnimeSequelC: AEm.add_field(name="Sequel:", value=AnimeSequelC, inline=False)
            if AnimeAlternateC: AEm.add_field(name="Alternate Version:", value=AnimeAlternateC, inline=False)
            if AnimeAdaptationC: AEm.add_field(name="Adaptation:", value=AnimeAdaptationC, inline=False)
            if AnimeSideC: AEm.add_field(name="Side Story:", value=AnimeSideC, inline=False)
            if AnimeSummaryC: AEm.add_field(name="Summary:", value=AnimeSummaryC, inline=False)
            if AnimeSpinC: AEm.add_field(name="Spin Off:", value=AnimeSpinC, inline=False)
            # AEm.add_field(name="\u200b", value="\u200b", inline=False)
            # try:
            #     AnimeOpening = "\n".join(AnimeGetmal.opening_themes)[:950]
            #     AEm.add_field( name="Opening Theme(s):", value=AnimeOpening, inline=False)
            # except TypeError: pass

            # try:
            #     AnimeEnding = ("\n".join(AnimeGetmal.ending_themes))[:950]
            #     AEm.add_field(name="Ending Theme(s):", value=AnimeEnding, inline=True)
            # except TypeError: pass
            await ctx.edit_original_response(embed=AEm)

        if not anime: await SendWait(ctx, "No Arguments :no_mouth:"); return
        AnimeInput = anime
        C = 0
        SrchAnime = []
        await ctx.response.send_message(embed=discord.Embed(title=":mag: Searching...", color=0x3FC0FF))
        SAEm = discord.Embed(title=f':mag: Results for "{AnimeInput}"', color=0x3FC0FF)
        for AnimeResult in MClient.search_anime(AnimeInput, limit=10):
            C += 1
            SAEm.add_field(name="\u200b", value=f"{C}. `{AnimeResult.title}`", inline=False)#**({AnimeResult.id})**
            SrchAnime.append(AnimeResult)
        await ctx.edit_original_response(embed=SAEm, view=Selector(getSel, exTimOt, list(range(1, C+1))))

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")


async def setup(DClient:CBotDClient) -> None:
   await DClient.add_cog(AnimeManga(DClient))