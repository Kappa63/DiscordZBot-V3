import discord
from typing import Optional, List
from Customs.UI.Selector import SelectionView
from Customs.Functions import checkClr

class NavigationView(discord.ui.View):
    def __init__(self, prevFunc, nextFunc, exitFunc, clrOnly:discord.Member = None) -> None:
        self.prevFunc = prevFunc
        self.nextFunc = nextFunc
        self.exitFunc = exitFunc
        self.clrOnly = clrOnly
        super().__init__(timeout=30)

    @discord.ui.button(label="<<", style=discord.ButtonStyle.primary, row=1)
    async def FarPrevPage(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if checkClr(self.clrOnly, interaction):
            await self.prevFunc(10)

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary, row=1)
    async def PrevPage(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if checkClr(self.clrOnly, interaction):
            await self.prevFunc(1)

    @discord.ui.button(label="x", style=discord.ButtonStyle.danger, row=1)
    async def ExitNav(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if checkClr(self.clrOnly, interaction):
            self.stop()
            await self.exitFunc()


    @discord.ui.button(label=">", style=discord.ButtonStyle.primary, row=1)
    async def NextPage(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if checkClr(self.clrOnly, interaction):
            await self.nextFunc(1)

    @discord.ui.button(label=">>", style=discord.ButtonStyle.primary, row=1)
    async def FarNextPage(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        if checkClr(self.clrOnly, interaction):
            await self.nextFunc(10)

    async def on_timeout(self) -> None:
        self.stop()
        await self.exitFunc()

class NavigationWithSelectorView(NavigationView):
    def __init__(self, prevFunc, nextFunc, exitFunc, selectFunc, navSt, labels:List[str], emojis:Optional[List[discord.Emoji]], clrOnly:discord.Member = None) -> None:
        self.selectFunc = selectFunc
        if emojis:
            self.lblEmoji = {k:v for k, v in zip(labels, emojis)}
            self.SELECTIONS = [discord.SelectOption(label=i, emoji=j) for i, j in zip(labels, emojis)]
        else:
            self.SELECTIONS = [discord.SelectOption(label=i) for i in labels]
        self.selector = discord.ui.Select(placeholder="Select Sorting", options=self.SELECTIONS, max_values=1, row=0)
        self.selector.callback = self.selectorCall
        self.initlz = False
        super().__init__(prevFunc, nextFunc, exitFunc, clrOnly)
        self.add_item(self.selector)
        self.navState(navSt)

    def navState(self, st:bool) -> None:
        for i in range(5):
            super().children[i].disabled = st

    async def selectorCall(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        if checkClr(self.clrOnly, interaction):
            self.selector.placeholder = f'{self.lblEmoji[self.selector.values[0]]} {self.selector.values[0]}'
            await interaction.edit_original_response(view=self)
            await self.selectFunc(self.selector.values[0])
            if(not self.initlz):
                self.initlz = True
                self.navState(False)
                await interaction.edit_original_response(view=self)
            