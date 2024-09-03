import discord
from discord.ext import commands
import requests
from Setup import OClient, FClient, PClient
from Customs.Functions import Threader, SendWait
from CBot import DClient as CBotDClient
from discord import app_commands

def PUBGDataEmbed(data, name) -> discord.Embed:
    PEm = discord.Embed(title=name, color=0x32110A)
    Combiner = lambda x, y: {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}
    Duo, Solo, Squad = Threader([Combiner]*3, [[data["duo"], data["duo-fpp"]], [data["solo"], data["solo-fpp"]], [data["squad"], data["squad-fpp"]]])
    PEm.add_field(name="***Solo:--***", 
                  value=f'**Wins:** `{Solo["wins"]:,}` \u2003 **Losses:** `{Solo["losses"]:,}` \u2003 **Top 10s:** `{Solo["top10s"]}`\n*Rounds Played:* `{Solo["roundsPlayed"]:,}` \u2003 *Longest Survival Time:* `{int(Solo["longestTimeSurvived"]):,}`\n\n**Kills:** `{Solo["kills"]:,}` \u2003 **Most Kills:** `{Solo["roundMostKills"]:,}`\n*Headshots:* `{Solo["headshotKills"]:,}` \u2003 *Damage Dealt:* `{int(Solo["damageDealt"]):,}`\n*Longest Kill:* `{int(Solo["longestKill"]):,}` \u2003 *Suicides:* `{Solo["suicides"]:,}`\n*Heals:* `{Solo["heals"]:,}` \u2003 *Revives:* `{Solo["revives"]}`',
                  inline=False)
    PEm.add_field(name="\u200b", value="\u200b", inline=False)
    PEm.add_field(name="***Duo:--***", 
                  value=f'**Wins:** `{Duo["wins"]:,}` \u2003 **Losses:** `{Duo["losses"]:,}` \u2003 **Top 10s:** `{Duo["top10s"]}`\n*Rounds Played:* `{Duo["roundsPlayed"]:,}` \u2003 *Longest Survival Time:* `{int(Duo["longestTimeSurvived"]):,}`\n\n**Kills:** `{Duo["kills"]:,}` \u2003 **Most Kills:** `{Duo["roundMostKills"]:,}`\n*Headshots:* `{Duo["headshotKills"]:,}` \u2003 *Damage Dealt:* `{int(Duo["damageDealt"]):,}`\n*Longest Kill:* `{int(Duo["longestKill"]):,}` \u2003 *Suicides:* `{Duo["suicides"]:,}`\n*Heals:* `{Duo["heals"]:,}` \u2003 *Revives:* `{Duo["revives"]}`',
                  inline=False)
    PEm.add_field(name="\u200b", value="\u200b", inline=False)
    PEm.add_field(name="***Squad:--***", 
                  value=f'**Wins:** `{Squad["wins"]:,}` \u2003 **Losses:** `{Squad["losses"]:,}` \u2003 **Top 10s:** `{Squad["top10s"]}`\n*Rounds Played:* `{Squad["roundsPlayed"]:,}` \u2003 *Longest Survival Time:* `{int(Squad["longestTimeSurvived"]):,}`\n\n**Kills:** `{Squad["kills"]:,}` \u2003 **Most Kills:** `{Squad["roundMostKills"]:,}`\n*Headshots:* `{Squad["headshotKills"]:,}` \u2003 *Damage Dealt:* `{int(Squad["damageDealt"]):,}`\n*Longest Kill:* `{int(Squad["longestKill"]):,}` \u2003 *Suicides:* `{Squad["suicides"]:,}`\n*Heals:* `{Squad["heals"]:,}` \u2003 *Revives:* `{Squad["revives"]}`',
                  inline=False)
    return PEm

class GameAPIs(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    @app_commands.command(name="osu", description="Profile of an OSU Player.")
    @app_commands.rename(usr="username")
    @app_commands.describe(usr="Player Username")
    @app_commands.checks.cooldown(1, 2)
    async def OSUuser(self, ctx:discord.Interaction, *, usr:str) -> None:
        if not usr: await SendWait(ctx, "No Username Given. Try add a Username First."); return
        User = OClient.get_user(usr)
        if User:
            OEm = discord.Embed(title=User.username,
                                description=f"**PP:** `{User.pp_raw:,}`\n**Level:** `{round(User.level,1)}`\n\n**Total Hours Played:** `{round(User.seconds_played/3600,2):,}`\n**Country({User.country}) Rank:** `{User.country_rank:,}`\n**Global Rank:** `{User.rank:,}`",
                                url=f"https://osu.ppy.sh/users/{User.user_id}", color=0xDA5B93)
            OEm.add_field(name="\u200b", value=f"**Ranked Score:** `{User.ranked_score:,}`\n**Total Score:** `{User.total_score:,}`", inline=False)
            OEm.add_field(name="\u200b", 
                          value=f"**Play Count:** `{User.playcount}`\n**50 Hits:** `{User.count_50:,}`\n**100 Hits:** `{User.count_100:,}`\n**300 Hits:** `{User.count_300:,}`\n**Total Hits:** `{User.count_300+User.count_100+User.count_50:,}`\n**Accuracy:** `{round(User.accuracy, 2)}`",
                          inline=True)
            OEm.add_field(name="\u200b", value="\u200b", inline=True)
            OEm.add_field(name="\u200b", 
                          value=f"**SS:** `{User.count_rank_ss:,}`\n**SSH:** `{User.count_rank_ssh:,}`\n**S:** `{User.count_rank_s:,}`\n**SH:** `{User.count_rank_sh:,}`\n**A:** `{User.count_rank_a:,}`",
                          inline=True)
            OEm.set_thumbnail(url=f"http://s.ppy.sh/a/{User.user_id}")
            OEm.set_footer(text=f"User ({User.username}) joined on {str(User.join_date)[:10]}")
            await ctx.response.send_message(embed=OEm)
        else: await SendWait(ctx, "No User Found. Try a Valid Username")

    @app_commands.command(name="fortnite", description="Profile of a Fortnite Player.")
    @app_commands.rename(usr="username")
    @app_commands.describe(usr="Player Username")
    @app_commands.checks.cooldown(1, 2)
    async def FortniteUser(self, ctx:discord.Interaction, *, usr:str) -> None:
        if not usr: await SendWait(ctx, "No Username Given. Try add a Username First."); return
        try:
            ImageStats = requests.get("https://fortnite-api.com/v2/stats/br/v2", params={"name": usr, "image": "all"}, headers=FClient).json()["data"]["image"]
            FEm = discord.Embed(title=f'Fortnite BR Stats for **`{usr}`**', color=0x00D8EB)
            FEm.set_image(url=ImageStats)
            await ctx.response.send_message(embed=FEm)
        except KeyError: await SendWait(ctx, "No User Found. Try a Valid Username")

    PUBGSlashes = app_commands.Group(name="pubg",  description="Main Command Group for PUBG.")

    @PUBGSlashes.command(name="all", description="All Time Profile of a PUBG Player.")
    @app_commands.rename(usr="username")
    @app_commands.describe(usr="Player Username")
    @app_commands.checks.cooldown(1, 2)
    async def GetAllTime(self, ctx:discord.Interaction, usr:str) -> None:
        if not usr: await SendWait(ctx, "No Username Given. Try add a Username First."); return
        try:
            a = requests.get("https://api.pubg.com/shards/steam/players", headers=PClient, params={"filter[playerNames]": usr}).json()
            Player = a["data"][0]
            PlayerID, PlayerName = Player["id"], Player["attributes"]["name"]
            AllData = requests.get(f"https://api.pubg.com/shards/steam/players/{PlayerID}/seasons/lifetime", headers=PClient).json()["data"]["attributes"]["gameModeStats"]
            await ctx.response.send_message(embed=PUBGDataEmbed(AllData, PlayerName))
        except KeyError: await SendWait(ctx, "No User Found. Try a Valid Username")

    @PUBGSlashes.command(name="season",  description="Season Profile of a PUBG Player.")
    @app_commands.rename(usr="username")
    @app_commands.describe(usr="Player Username")
    @app_commands.checks.cooldown(1, 2)
    async def GetSeason(self, ctx:discord.Interaction, usr:str) -> None:
        if not usr: await SendWait(ctx, "No Username Given. Try add a Username First."); return
        try:
            Player = requests.get("https://api.pubg.com/shards/steam/players", headers=PClient, params={"filter[playerNames]": usr}).json()["data"][0]
            PlayerID, PlayerName = Player["id"], Player["attributes"]["name"]
            SeasonID = requests.get("https://api.pubg.com/shards/steam/seasons", headers=PClient).json()["data"][-1]["id"]
            SeasonData = requests.get(f"https://api.pubg.com/shards/steam/players/{PlayerID}/seasons/{SeasonID}", headers=PClient).json()["data"]["attributes"]["gameModeStats"]
            await ctx.response.send_message(embed=PUBGDataEmbed(SeasonData, PlayerName))
        except KeyError: await SendWait(ctx, "No User Found. Try a Valid Username")

    # @commands.command(name="Roblox")
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def GetRobPlayer(self, ctx, *args):
    #     if not args: await SendWait(ctx, "No Username Given. Try add a Username First."); return
    #     try:
    #         NameInput = " ".join(args)
    #         User = await RLox.get_user_by_username(NameInput)
    #     except UserDoesNotExistError: await SendWait(ctx, "No User Found. Try a Valid Username"); return

    #     ImageUser = await User.thumbnails.get_avatar_image()
    #     FollowingN = await User.get_followings_count()
    #     FollowerN = await User.get_followers_count()
    #     FriendsN = await User.get_friends_count()
    #     Status = await User.get_status()
    #     Badges = "\n".join(i.name for i in await User.get_roblox_badges())

    #     REm = discord.Embed(title=f'{User.display_name} --- ID({User.id})',
    #                         description=User.description,
    #                         url=User.profile_url, color=0x33A3D7)
    #     REm.set_thumbnail(url=ImageUser)
    #     if User.is_banned: REm.add_field(name="***USER IS BANNED***", value=FollowingN, inline=False)
    #     if Status: REm.add_field(name="Status: ", value=Status, inline=False)
    #     REm.add_field(name="Following: ", value=FollowingN, inline=True)
    #     REm.add_field(name="Followers: ", value=FollowerN, inline=True)
    #     REm.add_field(name="Friends: ", value=FriendsN, inline=True)
    #     REm.add_field(name="Badges: ", value=f'_*{Badges}*_', inline=False)          
    #     await ctx.message.channel.send(embed=REm)

async def setup(DClient) -> None:
    await DClient.add_cog(GameAPIs(DClient))