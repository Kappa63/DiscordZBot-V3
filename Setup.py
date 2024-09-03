import dotenv
import os
# from discord.ext import commands
# import discord
# import tweepy
import malclient
# import twitch
# from discord import app_commands
# import asyncio
# import praw
# import asyncpraw
import giphpy as GApi
# import pymongo
import json
import time
from pymongo import MongoClient
import CBot
# from google_images_search import GoogleImagesSearch
# import pyyoutube
import imdb
# import pafy
# import datetime
from ossapi import OssapiV1
# import concurrent.futures as Cf

env = dotenv.find_dotenv()
dotenv.load_dotenv(env)

Cogs = ["Cogs.Randomizers", "Cogs.MainEvents", "Cogs.AnimeManga", "Cogs.WrittenStuff", "Cogs.GameAPIs", "Cogs.Games",
        #  "Cogs.HelpInfo", "Cogs.MongoDB",  "Cogs.Misc",
        "Cogs.Socials", "Cogs.OnlyMods", "Cogs.Nasa", "Cogs.Movies", "Cogs.Images", "Cogs.Google"]

DToken = os.environ["DISCORD_TOKEN_TIA"]

Cls = MongoClient(os.environ["MONGODB_URL"])
DbM = Cls["CBot"]
Eco = DbM["Eco"]
Rdt = DbM["Reddit"]

EcoOnSetData = {"achieved":[], "activeBadge":None, "badges":[]}

GClient = os.environ["GIPHY_KEY"]

CClient = {"X-CMC_PRO_API_KEY": os.environ["COINBASE_KEY"]}

NClient = {"country": "us", "apiKey": os.environ["NEWS_KEY"]}

# GiClient = GoogleImagesSearch(os.getenv("GCS_KEY"), os.getenv("CX_ID"))
def MalRefresher():
    if( (time.time() - float(os.environ["MAL_LAST_REFRESH"])) >= int(os.environ["MAL_REFRESH_TIME"]) ):
        MClient.refresh_bearer_token(client_id=os.environ["MAL_ID"], client_secret=os.environ["MAL_SECRET"], refresh_token=os.environ["MAL_REFRESH_TOKEN"])
        os.environ["MAL_LAST_REFRESH"] = str(time.time())
        dotenv.set_key(env, "MAL_LAST_REFRESH", os.environ["MAL_LAST_REFRESH"])
        os.environ["MAL_ACCESS_TOKEN"] = MClient._bearer_token
        dotenv.set_key(env, "MAL_ACCESS_TOKEN", os.environ["MAL_ACCESS_TOKEN"])
        os.environ["MAL_REFRESH_TOKEN"] = MClient.refresh_token
        dotenv.set_key(env, "MAL_REFRESH_TOKEN", os.environ["MAL_REFRESH_TOKEN"])

MClient = malclient.Client(client_id=os.environ["MAL_ID"], access_token=os.environ["MAL_ACCESS_TOKEN"], refresh_token=os.environ["MAL_REFRESH_TOKEN"], nsfw=True)
MalRefresher()
MALsearch = malclient.Fields(title=True, id=True, media_type=True)

PClient = {"Authorization": os.environ["PUBG_KEY"], "accept": "application/vnd.api+json"}

FClient = {"Authorization": os.environ["FORTNITE_KEY"]}

# twitter = tweepy.OAuthHandler(os.getenv("TWITTER_KEY"), os.getenv("TWITTER_SECRET"))
# twitter.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET"))
# Twitter = tweepy.API(twitter)

# Reddit = asyncpraw.Reddit(client_id=os.environ["REDDIT_ID"], client_secret=os.environ["REDDIT_SECRET"], user_agent="ZBot")

# Covid = COVID19Py.COVID19()

# YClient = pyyoutube.Api(api_key=os.environ["YOUTUBE_KEY"])

# THelix = twitch.TwitchHelix(os.getenv("TWITCH_ID"), os.getenv("TWITCH_SECRET"), use_cache=True, cache_duration=datetime.timedelta(minutes=3))

IMClient = imdb.IMDb()

OClient = OssapiV1(os.environ["OSU_KEY"])

# RLox = Roblox(os.getenv("ROBLOX_SECRET"))

# PatreonTiers = {
#     783250729686532126: "Tier 1 Casual",
#     783256987655340043: "Tier 2 Super",
#     784123230372757515: "Tier 3 Legend",
#     784124034559377409: "Tier 4 Ultimate",
# }

# RemoveExtra = lambda listRm, val: [value for value in listRm if value != val]

# GetVidDuration = lambda VidId: pafy.new(f"https://www.youtube.com/watch?v={VidId}").duration

# def RefreshGISClient():
#     global GiClient
#     del GiClient
#     GiClient = GoogleImagesSearch(os.getenv("GCS_KEY"), os.getenv("CX_ID"))

# def ErrorEmbeds(Type):
#     Descs = {"Vote": "This command is only for voters or patreon! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord) / [Vote](https://top.gg/bot/768397640140062721/vote)",
#              "Patreon": "This command is only for patreons supporters! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord)",
#              "PatreonT2": "This command is only for Tier 2 patreons (Super) supporters or above! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord)",
#              "PatreonT3": "This command is only for Tier 3 patreons (Legend) supporters or above! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord)",
#              "PatreonT4": "This command is only for Tier 4 patreons (Ultimate) supporters or above! [Official Server](https://discord.gg/V6E6prUBPv) / [Patreon](https://www.patreon.com/join/ZBotDiscord)"}
#     return discord.Embed(title="Oops",description= Descs[Type])

# def GetPatreonTier(UserID):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(UserID)
#         Roles = [discord.utils.get(MemGuild.roles, id=783250729686532126), discord.utils.get(MemGuild.roles, id=783256987655340043),
#                  discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return PatreonTiers[Role.id]
#     except AttributeError: pass

# class IsSetup(app_commands.CheckFailure): pass
# def ChSer(ctx:discord.Interaction):
#     if ColT.count_documents({"IDg": str(ctx.guild.id)}): return True
#     raise IsSetup("Unready")
# ChSerGuild = lambda guild: ColT.count_documents({"IDg": str(guild.id)})

# class IsMultiredditLimit(commands.CheckFailure): pass
# def ChMaxMultireddits(ctx):
#     TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
#     TierLimit = TierApplicable[GetPatreonTier(ctx.author.id)]
#     if Rdt.count_documents({"IDd": ctx.author.id}):
#         User = Rdt.find({"IDd": ctx.author.id})[0]
#         if len(User)-2 > TierLimit: raise IsMultiredditLimit("Too much")
#     return True

# class IsVote(commands.CheckFailure): pass
# async def ChVote(ctx):
#     if await CBot.TClient.get_user_vote(ctx.author.id): return True
#     else:
#         try:
#             MemGuild = CBot.DClient.get_guild(783250489843384341)
#             Mem = MemGuild.get_member(ctx.author.id)
#             Roles = [discord.utils.get(MemGuild.roles, id=783250729686532126), discord.utils.get(MemGuild.roles, id=783256987655340043),
#                      discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#             #- Roles.append(discord.utils.get(MemGuild.roles, id=783250729686532126))
#             #- Roles.append(discord.utils.get(MemGuild.roles, id=783256987655340043))
#             #- Roles.append(discord.utils.get(MemGuild.roles, id=784123230372757515))
#             #- Roles.append(discord.utils.get(MemGuild.roles, id=784124034559377409))
#             for Role in Roles:
#                 if Role in Mem.roles: return True
#         except AttributeError: pass
#         raise IsVote("No Vote")
# async def ChVoteUser(UserID):
#     if await CBot.TClient.get_user_vote(UserID): return True
#     else:
#         try:
#             MemGuild = CBot.DClient.get_guild(783250489843384341)
#             Mem = MemGuild.get_member(UserID)
#             Roles = [discord.utils.get(MemGuild.roles, id=783250729686532126), discord.utils.get(MemGuild.roles, id=783256987655340043),
#                      discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#             for Role in Roles:
#                 if Role in Mem.roles: return True
#         except AttributeError: pass
#         return False

# class IsPatreon(commands.CheckFailure): pass
# def ChPatreon(ctx):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(ctx.author.id)
#         Roles = [discord.utils.get(MemGuild.roles, id=783250729686532126), discord.utils.get(MemGuild.roles, id=783256987655340043),
#                  discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return True
#     except AttributeError: pass
#     raise IsPatreon("Not Patreon")
# def ChPatreonUser(UserID):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(UserID)
#         Roles = [discord.utils.get(MemGuild.roles, id=783250729686532126), discord.utils.get(MemGuild.roles, id=783256987655340043),
#                  discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return True
#     except AttributeError: pass
#     return False

# class IsPatreonT2(commands.CheckFailure): pass
# def ChPatreonT2(ctx):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(ctx.author.id)
#         Roles = [discord.utils.get(MemGuild.roles, id=783256987655340043), discord.utils.get(MemGuild.roles, id=784123230372757515), 
#                  discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return True
#     except AttributeError: pass
#     raise IsPatreonT2("Not Patreon")
# def ChPatreonUserT2(UserID):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(UserID)
#         Roles = [discord.utils.get(MemGuild.roles, id=783256987655340043), discord.utils.get(MemGuild.roles, id=784123230372757515), 
#                  discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return True
#     except AttributeError: pass
#     return False

# class IsPatreonT3(commands.CheckFailure): pass
# def ChPatreonT3(ctx):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(ctx.author.id)
#         Roles = [discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return True
#     except AttributeError: pass
#     raise IsPatreonT3("Not Patreon")
# def ChPatreonUserT3(UserID):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(UserID)
#         Roles = [discord.utils.get(MemGuild.roles, id=784123230372757515), discord.utils.get(MemGuild.roles, id=784124034559377409)]
#         for Role in Roles:
#             if Role in Mem.roles: return True
#     except AttributeError: pass
#     return False

# class IsPatreonT4(commands.CheckFailure): pass
# def ChPatreonT4(ctx):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(ctx.author.id)
#         Role = discord.utils.get(MemGuild.roles, id=784124034559377409)
#         if Role in Mem.roles: return True
#     except AttributeError: pass
#     raise IsPatreonT4("Not Patreon")
# def ChPatreonUserT4(UserID):
#     try:
#         MemGuild = CBot.DClient.get_guild(783250489843384341)
#         Mem = MemGuild.get_member(UserID)
#         Role = discord.utils.get(MemGuild.roles, id=784124034559377409)
#         if Role in Mem.roles: return True
#     except AttributeError: pass
#     return False
