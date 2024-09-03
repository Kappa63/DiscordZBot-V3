# from discord.ext import commands
import discord
import CBot
import asyncio
import gc
from Customs.UI.Navigation import NavigationView, NavigationWithSelectorView

class Navigator:
    def __init__(self, ctx:discord.Interaction, Items:discord.Embed, Type:str="#", EmbedAndContent:bool=False, ContItems:str=None, Main:bool=False, MainBed:discord.Embed=None, clrOnly:bool=False) -> None:
        self.ctx = ctx
        self.Items = Items
        self.Type = Type
        self.EmbedAndContent = EmbedAndContent
        self.ContItems = ContItems
        self.Main = Main
        self.MainBed = MainBed
        self.clrOnly = clrOnly

    async def previous(self, num:int) -> None:
        if self.ItemNum >= num:
            self.ItemNum -= num
            await self.Nav.edit(embed=self.Items[self.ItemNum])
            if self.EmbedAndContent: await self.Cont.edit(content=self.ContItems[self.ItemNum])
        elif self.MainBed: await self.Nav.edit(embed=self.MainBed); self.Main = True

    async def next(self, num:int) -> bool:
        if self.ItemNum < self.TotalItems - num:
            if self.Main: await self.Nav.edit(embed=self.Items[self.ItemNum]); self.Main = False
            else:
                self.ItemNum += num
                await self.Nav.edit(embed=self.Items[self.ItemNum])
                if self.EmbedAndContent: await self.Cont.edit(content=self.ContItems[self.ItemNum])
            return False
        else:
            return True
        
    async def resetWithNewItems(self, Items:discord.Embed):
        self.ItemNum = 0
        self.Items = Items
        await self.Nav.edit(embed=self.Items[self.ItemNum])

    async def selectPage(self) -> None:
        def ChCHEmFN(MSg) -> bool:
            MesS = MSg.content.lower()
            RsT = False
            try:
                if int(MSg.content): RsT = True
            except ValueError:
                if MesS in ["cancel", "c"]: RsT = True
            return MSg.guild.id == self.ctx.guild.id and MSg.channel.id == self.ctx.channel.id and RsT
        
        TempNG = await self.ctx.response.send_message('Choose a number to open navigate to ItemNum. "c" or "cancel" to exit navigation.')
        try:
            ResE = await CBot.BotClient.wait_for("message", check=ChCHEmFN, timeout=10)
            await TempNG.delete()
            await ResE.delete()
            try:
                pG = int(ResE.content)
                if 0 < pG <= self.TotalItems - 1: self.ItemNum = pG - 1
                elif pG < 1:
                    self.ItemNum = 0
                    pass
                else: self.ItemNum = self.TotalItems - 1
            except: pass
            await self.Nav.edit(embed=self.Items[self.ItemNum])
            if self.EmbedAndContent: await self.Cont.edit(content=self.ContItems[self.ItemNum])
        except asyncio.TimeoutError:
            await TempNG.edit("Request Timeout")
            await asyncio.sleep(5)
            await TempNG.delete()

class ReactionNavigator(Navigator):
    async def setup(self) -> None:
        self.ItemNum = 0
        if not self.Main: self.Nav = await self.ctx.followup.send(embed=self.Items[self.ItemNum])
        else: self.Nav = await self.ctx.followup.send(embed=self.MainBed)
        if self.EmbedAndContent: self.Cont = await self.ctx.response.send_message(content=self.ContItems[self.ItemNum])
        self.TotalItems = len(self.Items)
        await self.Nav.add_reaction("⬅️")
        await self.Nav.add_reaction("❌")
        await self.Nav.add_reaction("➡️")
        if self.Type == "#": await self.Nav.add_reaction("#️⃣")
        
    async def exitNavigation(self) -> None:
        await self.Nav.remove_reaction("⬅️", CBot.BotClient.user)
        await self.Nav.remove_reaction("❌", CBot.BotClient.user)
        await self.Nav.remove_reaction("➡️", CBot.BotClient.user)
        if self.Type == "#": await self.Nav.remove_reaction("#️⃣", CBot.BotClient.user)

    async def autoRun(self) -> None:
        def ChCHEm (RcM, RuS):
            return (not RuS.bot) and RcM.message == self.Nav and str(RcM.emoji) in ["⬅️", "❌", "➡️", "#️⃣"]
    
        await self.setup()
        while True:
            try:
                Res = await CBot.BotClient.wait_for("reaction_add", check=ChCHEm, timeout=30)
                await self.Nav.remove_reaction(Res[0].emoji, Res[1])
                if Res[0].emoji == "⬅️":
                    await self.previous()
                elif Res[0].emoji == "➡️":
                    if(await self.next()):
                        await self.exitNavigation()
                        break
                elif Res[0].emoji == "#️⃣" and self.Type == "#":
                    await self.selectPage()
                elif Res[0].emoji == "❌":
                    await self.exitNavigation()
                    break
            except asyncio.TimeoutError:
                await self.exitNavigation()

class ButtonNavigator(Navigator):
    async def setup(self) -> None:
        self.ItemNum = 0
        self.Nav = await self.ctx.followup.send(embed=((self.Items[self.ItemNum]) if not self.Main else self.MainBed), view=NavigationView(self.previous, self.next, self.exitNavigation, self.ctx.user if self.clrOnly else None))
        if self.EmbedAndContent: self.Cont = await self.ctx.followup.send(content=self.ContItems[self.ItemNum])
        self.TotalItems = len(self.Items)

    async def exitNavigation(self) -> None:
        await self.Nav.edit(view=None)

    async def autoRun(self) -> None:
        await self.setup()

class SortableButtonNavigator(Navigator):
    def __init__(self, onSlct, lbls, emjis, ctx:discord.Interaction, Type:str="#", EmbedAndContent:bool=False, ContItems:str=None, Main:bool=False, MainBed:discord.Embed=None, clrOnly:bool=False) -> None:
        self.onSlct = onSlct
        self.Cache = {}
        self.lbls = lbls
        self.emjis = emjis
        super().__init__(ctx, [], Type, EmbedAndContent, ContItems, Main, MainBed, clrOnly)

    async def setup(self) -> None:
        self.ItemNum = 0
        self.Nav = await self.ctx.followup.send(embed=discord.Embed(title="Select Sorting..."), 
                                                view=NavigationWithSelectorView(self.previous, self.next, self.exitNavigation, self.slctUpdt, True, self.lbls, self.emjis, self.ctx.user if self.clrOnly else None))
        if self.EmbedAndContent: self.Cont = await self.ctx.followup.send(content=self.ContItems[self.ItemNum])
        self.TotalItems = len(self.Items)

    async def slctUpdt(self, srt:str) -> None:
        await self.Nav.edit(embed=discord.Embed(title="Getting Posts..."))
        if(srt not in self.Cache):
            self.Cache[srt] = await self.onSlct(srt)
        if(self.Cache[srt]):
            self.TotalItems = len(self.Cache[srt])
            await self.resetWithNewItems(self.Cache[srt])
        else:
            await self.Nav.edit(embed=discord.Embed(title="Empty or Doesn't Exist..."))

    async def exitNavigation(self) -> None:
        self.Cache = None
        await self.Nav.edit(view=None)
        del self
        gc.collect()

    async def autoRun(self) -> None:
        await self.setup()