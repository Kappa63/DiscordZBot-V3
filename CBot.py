import discord
from discord.ext import commands
# import dbl
from Setup import Cogs, DToken

class DClient(commands.Bot):
    StaffChannel = None
    Me = None
    def __init__(self, Cogs) -> None:
        REqInt = discord.Intents.default()
        REqInt.members = True
        self.LoadedCogs = Cogs
        super().__init__(case_insensitive=True, command_prefix=["Z","z"], intents=REqInt, help_command=None)
   
    async def setup_hook(self) -> None:
        for Cog in self.LoadedCogs: 
            await self.load_extension(Cog)
        print("Cogs Loaded...")
        return await super().setup_hook()
    
    async def reload_all_cogs(self) -> None:
        for Cog in self.LoadedCogs: 
            await self.reload_extension(Cog)
        print("Cogs Reloaded...")

    async def reload_cogs(self, cogsRe) -> None:
        for Cog in cogsRe: 
            await self.reload_extension(Cog)
        print("Cogs Reloaded...")

    async def unload_cogs(self, cogsRe) -> None:
        for Cog in cogsRe: 
            try:
                await self.unload_extension(Cog)
                self.LoadedCogs.remove(Cog)
            except:
                pass
        print("Cogs Unloaded...")

    async def load_cogs(self, cogsRe) -> None:
        for Cog in cogsRe: 
            try:
                await self.load_extension(Cog)
                self.LoadedCogs.add(Cog)
            except:
                pass

        print("Cogs Loaded...")

# TClient = dbl.client.DBLClient(bot=DClient, token=os.getenv("DBL_TOKEN"), autopost=True)

#_ @DClient.check
#_ async def ChModDown(ctx):
#_     OpenState = open("OpenState.txt")
#_     State = OpenState.readlines()
#_     OpenState.close()
#_     if ("".join(State) == "Down") and ctx.author.id not in [507212584634548254, 443986051371892746, 224809178793771009]: raise Ignore("Ignore")
#_     return True
# Cogs = ["Cogs.Misc", "Cogs.MongoDB", "Cogs.Covid", "Cogs.Nasa", "Cogs.Socials", "Cogs.AnimeManga",
#         "Cogs.HelpInfo", "Cogs.Randomizers", "Cogs.OnlyMods", "Cogs.MainEvents", 
#         "Cogs.Images","Cogs.WrittenStuff", "Cogs.Movies", "Cogs.Games", "Cogs.GameAPIs", "Cogs.Google"]

# @BotClient.check
# async def ChBot(ctx:discord.Interaction):
#     if ctx.user.bot: raise IsBot("Bot")
#     return True

# @BotClient.check
# async def ChDM(ctx):
#     if ctx.guild: return True
#     raise Ignore("Ignore")

BotClient = DClient(Cogs=Cogs)
BotClient.run(DToken)
