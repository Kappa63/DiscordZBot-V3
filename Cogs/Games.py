import discord
from discord.ext import commands
from discord import app_commands
from CBot import DClient as CBotDClient
from Customs.UI.TicTacToe import TicTacToeView as TTTView
from typing import Optional
from Customs.Functions import SendWait
from pymongo.collection import ReturnDocument 

# def SudokuBoardMaker(Title, BoardName, Board, Difficulty):
#     DigitReplace = [":white_large_square:", ":one:", ":two:", ":three:", ":four:", ":five:", 
#                     ":six:", ":seven:", ":eight:", ":nine:"]
#     SEm = discord.Embed(title=f"{Title} (ID: {BoardName})", description=f"`Difficulty: {Difficulty.upper()}`", color=0x83E42C)
#     R = 0
#     FormSq1 = ""
#     for Row in Board:
#         R += 1
#         D = 0
#         for Digit in Row:
#             D += 1
#             if D > 3:
#                 FormSq1 += " \u200b "
#                 D = 1
#             FormSq1 += DigitReplace[Digit]
#         if R < 3: FormSq1 += "\n"
#         else:
#             R = 0
#             SEm.add_field(name="\u200b", value=FormSq1, inline=False)
#             FormSq1 = ""
#     SEm.set_footer(text='"zhelp sudoku" for more info')
#     return SEm

# def NextSq(grid, i, j):
#     for x in range(i,9):
#         for y in range(j,9):
#             if grid[x][y] == 0: return x,y
#     for x in range(0,9):
#         for y in range(0,9):
#             if grid[x][y] == 0: return x,y
#     return -1,-1

# def CheckSudoku(grid, i, j, e):
#     RowCheck = all([e != grid[i][x] for x in range(9)])
#     if RowCheck:
#         ColumnCheck = all([e != grid[x][j] for x in range(9)])
#         if ColumnCheck:
#             TopX, TopY = 3 *(i//3), 3 *(j//3)
#             for x in range(TopX, TopX+3):
#                 for y in range(TopY, TopY+3):
#                     if grid[x][y] == e: return False
#             return True
#     return False

# def SudokuSolver(grid, i=0, j=0):
#     i,j = NextSq(grid, i, j)
#     if i == -1: return True
#     for e in range(1,10):
#         if CheckSudoku(grid,i,j,e):
#             grid[i][j] = e
#             if SudokuSolver(grid, i, j): return True
#             grid[i][j] = 0
#     return False

class Games(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    # @commands.command(name="sudoku")
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def PlaySudoku(self, ctx:commands.Context, *args) -> None:
    #     ChCHEm = lambda RcM, RuS: not RuS.bot and RcM.message == OriginalBoard and str(RcM.emoji) in ["👁️", "❌"]
        
    #     Difficulty = list(args)[0].lower() if args else "random"
    #     RanChars = "abcdefghijklmnopqrstuvwxyz1234567890"
    #     BoardName = "".join((random.choice(RanChars) for i in range(5)))
    #     if Difficulty not in ["easy", "hard", "medium", "random"]: await SendWait(ctx, "Not valid difficulty :confused:"); return
    #     SudokuBoard = requests.get(f"https://sugoku.onrender.com/board?difficulty={Difficulty}").json()["board"]
    #     #- JSONboard = SudokuBoard.json()["board"]
    #     OriginalBoard = await ctx.response.send_message(embed=SudokuBoardMaker("Sudoku", BoardName, SudokuBoard, Difficulty))
    #     await OriginalBoard.add_reaction("👁️")
    #     await OriginalBoard.add_reaction("❌")
    #     try:
    #         ReaEm = await self.DClient.wait_for("reaction_add", check=ChCHEm, timeout=3600)
    #         await OriginalBoard.remove_reaction(ReaEm[0].emoji, ReaEm[1])
    #         if ReaEm[0].emoji == "👁️":
    #             SudokuSolver(SudokuBoard)
    #             await ctx.response.send_message(embed=SudokuBoardMaker("Solution", BoardName, SudokuBoard, Difficulty))
    #         await OriginalBoard.remove_reaction("👁️", self.DClient.user)
    #         await OriginalBoard.remove_reaction("❌", self.DClient.user)
    #     except asyncio.TimeoutError:
    #         SudokuSolver(SudokuBoard)
    #         await ctx.message.channel.send(embed=SudokuBoardMaker("Solution", BoardName, SudokuBoard, Difficulty))

    @app_commands.command(name="tictactoe", description="Start a Game of TicTacToe with Another User.")
    @app_commands.rename(usr="user")
    @app_commands.describe(usr="@ User to Start Game Against")
    @app_commands.checks.cooldown(1, 3)
    async def PlayTTT(self, ctx:discord.Interaction, usr:discord.Member) -> None:
        async def noP(pl, fin):
            await ctx.edit_original_response(content=f"{pl.mention} did not Respond. Game Ended.", view=fin)
        if (usr and not usr.bot and usr.id != ctx.user.id):
            Table = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
            Players = [ctx.user, usr] # ctx.message.mentions[0]
            PlayerAssign = {Players[0]: "x", Players[1]: "o"}
            await ctx.response.send_message(content=f"{Players[0].mention}'s Turn", view=TTTView(Players[0], Players[1], noP)) # embed=TTTBoardMaker(Table, Players[0], Players[1])
        else: await SendWait(ctx, "No second player mentioned or Mentioned a bot :slight_frown:!")

    # @commands.command(aliases=["cptd", "chesspuzzleoftheday"])
    # @commands.cooldown(1, 3, commands.BucketType.user)
    # async def SendCPTD(self, ctx):
    #     GetCPTD = requests.get("https://api.chess.com/pub/puzzle", headers={"Accept": "application/json"}, params={'User-Agent': 'mycontact@gmail.com'})
    #     print(GetCPTD)
    #     CEm = discord.Embed(title=GetCPTD["title"], description=f'[Daily Puzzle]({GetCPTD["url"]}) from [Chess.com](https://www.chess.com/)', color=0x6C9D41)
    #     CEm.set_image(url=GetCPTD["image"])
    #     await ctx.response.send_message(embed=CEm)

async def setup(DClient):
    await DClient.add_cog(Games(DClient))