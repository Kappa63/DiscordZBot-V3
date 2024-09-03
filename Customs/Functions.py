# import datetime
import concurrent.futures as Cf
import discord
from typing import List
from discord import app_commands
from Setup import MalRefresher
from discord.ext import commands

async def SendWait(ctx:discord.Interaction, Notice:str) -> None: await ctx.followup.send(embed=discord.Embed(title=Notice))
async def SendWaitCMDs(ctx:commands.Context, Notice:str) -> None: await ctx.send(embed=discord.Embed(title=Notice))

def FormatTime(SecondsFormat:int) -> str:
    Day = 0
    Hour = 0
    Min = 0
    while SecondsFormat >= 60:
        Min += 1
        if Min == 60:
            Hour += 1
            Min -= 60
        if Hour == 24:
            Day += 1
            Hour -= 24
        SecondsFormat -= 60
    if Day != 0: return f"{Day}d {Hour}h {Min}m {SecondsFormat}s"
    elif Hour != 0: return f"{Hour}h {Min}m {SecondsFormat}s"
    elif Min != 0: return f"{Min}m {SecondsFormat}s"
    else: return f"{SecondsFormat}s"

# def TimeTillMidnight() -> int:
#     Now = datetime.datetime.now()
#     return (10 + ((24 - Now.hour - 1) * 60 * 60) + ((60 - Now.minute - 1) * 60) + (60 - Now.second))

def Threader(FunctionList, ParameterList) -> (list | bool):
    try:
        with Cf.ThreadPoolExecutor() as Execute:
            Pool = [Execute.submit(Func, *Param) for Func, Param in zip(FunctionList, ParameterList)]
            Results = [Execution.result() for Execution in Pool]
    except:
        return False
    return Results

def checkClr(clr:discord.Member, i:discord.Interaction) -> bool:
    return (not clr or clr.id == i.user.id)

class IsAdmin(app_commands.CheckFailure): pass
def ChAdmin(ctx:discord.Interaction):
    if ctx.user.guild_permissions.administrator: return True
    raise IsAdmin("Normie")

class Ignore(commands.CheckFailure): pass
def ChDev(ctx:commands.Context) -> bool:
    return ctx.author.id == 443986051371892746
    # raise Ignore("Ignore")

def RefreshMAL(ctx:discord.Interaction) -> bool:
    MalRefresher()
    return True

class IsNSFW(app_commands.CheckFailure): pass
def ChNSFW(ctx:discord.Interaction):
    if ctx.channel.is_nsfw(): return True
    raise IsNSFW("Not Safe")

class IsBot(app_commands.CheckFailure): pass