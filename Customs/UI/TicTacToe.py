import discord
import numpy as np

class TicTacToeView(discord.ui.View):
    def __init__(self, usr1:discord.User, usr2:discord.User, onTout) -> None: 
        self.usr1 = usr1
        self.usr2 = usr2
        self.onTout = onTout
        self.Trn = 1
        super().__init__(timeout=30)

    def TTTWinCheck(self):
        B = [i.label for i in self.children]
        Board = [B[i:i+3] for i in range(0, len(B), 3)] 
        if any(any(i in j for j in [Board, np.dstack(Board)[0].tolist(), [np.diag(Board).tolist(), np.diag(np.fliplr(Board)).tolist()]]) for i in [["O"]*3, ["X"]*3]): return True
        return False
    
    async def Play(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if((self.usr1 if self.Trn%2 else self.usr2).id == interaction.user.id):
            button.label = "X" if self.Trn%2 else "O"
            button.style = discord.ButtonStyle.green if self.Trn%2 else discord.ButtonStyle.red
            button.disabled = True
            if(self.TTTWinCheck()):
                for i in self.children:
                    i.disabled = True
                await interaction.response.edit_message(content=f"{(self.usr1 if self.Trn%2 else self.usr2).mention} WINS!!!",view=self)
                return
            if(self.Trn >= 9):
                await interaction.response.edit_message(content=f"It's a DRAW!!!", view=self)
                return
            self.Trn+=1
            await interaction.response.edit_message(content=f"{(self.usr1 if self.Trn%2 else self.usr2).mention}'s Turn",view=self)
            return
        await interaction.response.defer()

    @discord.ui.button(label="1", style=discord.ButtonStyle.secondary, row=1)
    async def Sq1(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.Play(interaction, button)

    @discord.ui.button(label="2", style=discord.ButtonStyle.secondary, row=1)
    async def Sq2(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.Play(interaction, button)
        
    @discord.ui.button(label="3", style=discord.ButtonStyle.secondary, row=1)
    async def Sq3(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.Play(interaction, button)

    @discord.ui.button(label="4", style=discord.ButtonStyle.secondary, row=2)
    async def Sq4(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.Play(interaction, button)

    @discord.ui.button(label="5", style=discord.ButtonStyle.secondary, row=2)
    async def Sq5(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.Play(interaction, button)

    @discord.ui.button(label="6", style=discord.ButtonStyle.secondary, row=2)
    async def Sq6(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.Play(interaction, button)

    @discord.ui.button(label="7", style=discord.ButtonStyle.secondary, row=3)
    async def Sq7(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.Play(interaction, button)

    @discord.ui.button(label="8", style=discord.ButtonStyle.secondary, row=3)
    async def Sq8(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.Play(interaction, button)

    @discord.ui.button(label="9", style=discord.ButtonStyle.secondary, row=3)
    async def Sq9(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.Play(interaction, button)

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        self.stop()
        await self.onTout(self.usr1 if self.Trn%2 else self.usr2, self)