import discord
from discord import app_commands
from discord.ext import commands
from prawcore import NotFound, Forbidden
from CBot import DClient as CBotDClient
from Setup import Rdt
from Customs.Functions import SendWait, Threader
from Customs.Navigators import ButtonNavigator as Navigator
from Customs.Navigators import SortableButtonNavigator as SortedNav
import datetime
import numpy as np
import asyncpraw
import os

def RedditbedMaker(SubCpoS, Subname, Nsfchannel:bool, Type:str="R", PostNum:int=0, TotalPosts:int=0) -> discord.Embed:
    PostTitle = SubCpoS.title[:253]
    PostText = SubCpoS.selftext[:1021]
    if PosType(SubCpoS):
        if SubCpoS.over_18 and Nsfchannel:
            REm = discord.Embed(title=PostTitle, description=f"Upvote Ratio: {SubCpoS.upvote_ratio} // Post is NSFW", color=0x8B0000)
            if Type == "S": REm.add_field(name=f"`Page: {PostNum+1}/{TotalPosts}`", value="\u200b",inline=True)
            if PostText: REm.add_field(name="Body", value=PostText, inline=False)
            REm.add_field(name="Post: ", value=SubCpoS.url, inline=True)
        elif not Nsfchannel and SubCpoS.over_18:
            REm = discord.Embed(title="***NOT NSFW CHANNEL***", description="Post is NSFW", color=0x8B0000)
            REm.add_field(name="NSFW: ", value="This channel isn't NSFW. No NSFW here", inline=False)
        else:
            REm = discord.Embed(title=PostTitle, description=f"Upvote Ratio: {SubCpoS.upvote_ratio} // Post is Clean", color=0x8B0000)
            if Type == "S": REm.add_field(name=f"`Page: {PostNum+1}/{TotalPosts}`", value="\u200b", inline=True)
            if PostText: REm.add_field(name="Body", value=PostText, inline=False)
            REm.add_field(name="Post: ", value=SubCpoS.url, inline=True)
    else:
        NSfw = SubCpoS.over_18
        if SubCpoS.over_18 and Nsfchannel: REm = discord.Embed(title=PostTitle, description=f"Upvote Ratio: {SubCpoS.upvote_ratio} // Post is NSFW", color=0x8B0000)
        elif not Nsfchannel and SubCpoS.over_18: REm = discord.Embed(title="***NOT NSFW CHANNEL***", description="Post is NSFW", color=0x8B0000)
        else: REm = discord.Embed(title=PostTitle, description=f"Upvote Ratio: {SubCpoS.upvote_ratio} // Post is Clean", color=0x8B0000)
        if Type == "S":REm.add_field(name=f"`Post: {PostNum+1}/{TotalPosts}`", value="\u200b", inline=True)
        C = 0
        if (NSfw and Nsfchannel) or not NSfw:
            try:
                GaLpos = SubCpoS.gallery_data["items"]
                for ImgPoGa in GaLpos:
                    FiPoS = SubCpoS.media_metadata[ImgPoGa["media_id"]]
                    if FiPoS["e"] == "Image":
                        REm.add_field(name="\u200b", value=f"The original post is a gallery [click here]({SubCpoS.url}) to view the rest of the post", inline=False)
                        REm.set_image(url=FiPoS["p"][-1]["u"])
                        break
            except AttributeError:
                if SubCpoS.url.endswith(".gifv"):
                    REm.add_field(name="\u200b", value=f"The original post is a video(imgur) [click here]({SubCpoS.url}) to view the original", inline=False)
                    REm.set_image(url=SubCpoS.url[:-1])
                elif SubCpoS.url[-4:] in [".jpg", ".png", ".gif", "jpeg"]: REm.set_image(url=SubCpoS.url)
                else:
                    if "v.redd.it" in SubCpoS.url: EmbOri(REm, "video (reddit)", SubCpoS)
                    elif "youtu.be" in SubCpoS.url or "youtube.com" in SubCpoS.url: EmbOri(REm, "video (youtube)", SubCpoS)
                    elif "gfycat" in SubCpoS.url: EmbOri(REm, "video (gfycat)", SubCpoS)
                    elif "redgifs" in SubCpoS.url: EmbOri(REm, "video (redgifs)", SubCpoS)
                    else: EmbOri(REm, "webpage", SubCpoS)
        else: REm.add_field(name="NSFW: ", value="This isn't an NSFW channel. No NSFW allowed here.", inline=False)
    if Type != "S": REm.set_footer(text=f"From r/{SubCpoS.subreddit.display_name}")
    REm.set_author(name=f"*By u/{SubCpoS.author}*")
    return REm

# def YoutubebedMaker(VidID, Channel, VidNum, VidsTotal):
#     try:
#         try: Vid = YClient.get_video_by_id(video_id=VidID).items[0]
#         except: return
#         YLEm = discord.Embed(title=Vid.snippet.title, description=Vid.snippet.description.split("\n")[0], url=f"https://www.youtube.com/watch?v={VidID}", color=0xFF0000)
#         YLEm.set_thumbnail(url=Vid.snippet.thumbnails.high.url)
#         YLEm.add_field(name=f"`Video: {VidNum+1}/{VidsTotal}`", value="\u200b", inline=False)
#         if Vid.snippet.liveBroadcastContent == "live": YLEm.add_field(name="**CURRENTLY LIVE**", value="\u200b", inline=True)
#         else:
#             YLEm.add_field(name=f"Upload Date: {Vid.snippet.publishedAt[:10]}", value="\u200b", inline=False)
#             YLEm.add_field(name=f"Duration: {GetVidDuration(VidID)}", value="\u200b", inline=False)
#         if hasattr(Vid.statistics, "viewCount"): YLEm.add_field(name="Views :eye:", value=f"{int(Vid.statistics.viewCount):,}", inline=True)
#         else: YLEm.add_field(name="Views :eye:", value="Disabled", inline=True)
#         YLEm.add_field(name="\u200b", value="\u200b", inline=True)
#         if hasattr(Vid.statistics, "commentCount"): YLEm.add_field(name="Comments :speech_balloon:", value=f"{int(Vid.statistics.commentCount):,}", inline=True)
#         else: YLEm.add_field(name="Comments :speech_balloon:", value="Disabled", inline=True)
#         try:
#             if hasattr(Vid.statistics, "likeCount"): YLEm.add_field(name="Likes :thumbsup:", value=f"{int(Vid.statistics.likeCount):,}", inline=True)
#             else: YLEm.add_field(name="Likes :thumbsup:", value="Disabled", inline=True)
#         except: pass
#         YLEm.add_field(name="\u200b", value="\u200b", inline=True)
#         try:
#             if hasattr(Vid.statistics, "dislikeCount"): YLEm.add_field(name="Dislikes :thumbsdown:", value=f"{int(Vid.statistics.dislikeCount):,}", inline=True)
#             else: YLEm.add_field(name="Dislikes :thumbsdown:", value="Disabled", inline=True)
#         except: pass
#         YLEm.add_field(name="\u200b", value="\u200b", inline=False)
#         if not Channel.statistics.hiddenSubscriberCount: 
#             YLEm.set_footer(text=f"{Channel.snippet.title} / Subs: {int(Channel.statistics.subscriberCount):,} / Videos: {int(Channel.statistics.videoCount):,}", 
#                             icon_url=Channel.snippet.thumbnails.high.url)
#         else: 
#             YLEm.set_footer(text=f"{Channel.snippet.title} / Videos: {int(Channel.statistics.videoCount):,}\n\nNeed help navigating? zhelp navigation", 
#                             icon_url=Channel.snippet.thumbnails.high.url)

#     except OSError: 
#         YLEm = discord.Embed(title="Video Age Restricted", description="", color=0xFF0000)
#         YLEm.add_field(name=f"`Video: {VidNum+1}/{VidsTotal}`", value="\u200b", inline=False)
#     return YLEm
    

# def TwitterbedMaker(TWprofile, IsVerified, TwTtype, TWtimeline, TwTNum, TwTtotal):
#     TEmE = discord.Embed(title=f"@{TWprofile.screen_name} / {TWprofile.name} {IsVerified}", description=TwTtype, color=0x0384FC)
#     TEmE.set_thumbnail(url=TWprofile.profile_image_url_https)
#     TEmE.add_field(name=f"{TwTtype} on: ", value=TWtimeline.created_at, inline=False)
#     TEmE.add_field(name=f"`{TwTNum+1}/{TwTtotal}`", value="\u200b", inline=False)
#     TEmE.add_field(name="Retweets: ", value=f"{TWtimeline.retweet_count:,}", inline=True)
#     TEmE.add_field(name="Likes: ", value=f"{TWtimeline.favorite_count:,}", inline=True)
#     if TwTtype == "Retweet":
#         try:
#             if hasattr(TWtimeline.retweeted_status, "extended_entities"): TEmE.set_image(url=TWtimeline.retweeted_status.extended_entities["media"][0]["media_url_https"])
#             TEmE.add_field(name=f"Retweeted Body (By: {Twitter.get_user(user_id = TWtimeline.retweeted_status.user.id).screen_name}): ", 
#                            value=TWtimeline.retweeted_status.full_text, inline=False)
#         except tweepy.error.TweepError: TEmE.add_field(name="On (By: --Deleted--): ", value="--Deleted--", inline=False)
#     elif TwTtype == "Quote":
#         try:
#             if hasattr(TWtimeline.quoted_status, "extended_entities"): TEmE.set_image(url=TWtimeline.quoted_status.extended_entities["media"][0]["media_url_https"])
#             TEmE.add_field(name="Main Body: ", value=TWtimeline.full_text, inline=False)
#             TEmE.add_field(name=f"Quoted Body (By: {Twitter.get_user(user_id = TWtimeline.quoted_status.user.id).screen_name}): ", 
#                            value=TWtimeline.quoted_status.full_text, inline=False)
#         except tweepy.error.TweepError: TEmE.add_field(name="On (By: --Deleted--): ", value="--Deleted--", inline=False)
#     elif TwTtype == "Tweet":
#         if hasattr(TWtimeline, "extended_entities"): TEmE.set_image(url=TWtimeline.extended_entities["media"][0]["media_url_https"])
#         TEmE.add_field(name="Tweet Body: ", value=TWtimeline.full_text, inline=False)
#     elif TwTtype == "Comment":
#         TEmE.add_field(name="Comment Body: ", value=TWtimeline.full_text, inline=False)
#         try:
#             TwCO = Twitter.get_status(id=TWtimeline.in_reply_to_status_id, trim_user=True,  tweet_mode="extended")
#             if hasattr(TwCO, "extended_entities"): TEmE.set_image(url=TwCO.extended_entities["media"][0]["media_url_https"])
#             TEmE.add_field(name=f"On (By: {TWtimeline.in_reply_to_screen_name}): ", value=TwCO.full_text, inline=False)
#         except tweepy.error.TweepError: TEmE.add_field(name="On (By: --Deleted--): ", value="--Deleted--", inline=False)
#     TEmE.set_footer(text="Need help navigating? zhelp navigation")
#     return TEmE

# def ChTwTp(TWtimeline):
#     if hasattr(TWtimeline, "retweeted_status") and TWtimeline.retweeted_status: return "Retweet"
#     elif hasattr(TWtimeline, "quoted_status") and TWtimeline.quoted_status: return "Quote"
#     elif hasattr(TWtimeline, "in_reply_to_status_id") and TWtimeline.in_reply_to_status_id: return "Comment"
#     else: return "Tweet"

def EmbOri(REm:discord.Embed, Type:str, SubCpoS) -> discord.Embed:
    REm.add_field(name="\u200b", value=f"The original post is a {Type} [click here]({SubCpoS.url}) to view the original", inline=False)
    try:
        REm.set_image(url=SubCpoS.preview["images"][-1]["source"]["url"])
    except: 
        return REm
    return REm



PosType = lambda Sub: Sub.is_self

class Socials(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient
        self.Reddit = asyncpraw.Reddit(client_id=os.environ["REDDIT_ID"], client_secret=os.environ["REDDIT_SECRET"], user_agent="ZBot by u/Kamlin333")

    # @commands.group(name="twitch", invoke_without_command=True)
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def TTwitch(self, ctx, *args):
    #     if not args: await SendWait(ctx, "No Username"); return    
    #     try:
    #         UHelix = THelix.user(" ".join(args))
    #         Name = UHelix.display_name
    #         Desc = UHelix.description
    #         Type = UHelix.broadcaster_type.capitalize()
    #         PImg = UHelix.profile_image_url
    #         HImg = UHelix.offline_image_url
    #         TViews = UHelix.view_count
    #         IsLive = UHelix.is_live
    #         ThEm = discord.Embed(title = Type, description = Desc, color = 0x9147FF)
    #         ThEm.set_author(name=Name, icon_url=PImg, url=f'https://www.twitch.tv/{Name}')
    #         ThEm.set_thumbnail(url=HImg)
    #         ThEm.add_field(name = "Total Views: ", value = f'{TViews:,}', inline=False)
    #         if IsLive: ThEm.add_field(name = ":red_circle: CURRENTLY LIVE :red_circle:", value="\u200b", inline=False)
    #         await ctx.response.send_message(embed = ThEm)
    #     except AttributeError: await SendWait(ctx, "User Not Found")

    # @TTwitch.command(name="stream")
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def StreamerStream(self, ctx, *args):
    #     if not args: await SendWait(ctx, "No Username"); return
    #     try:
    #         await SendWait(ctx, ":busts_in_silhouette: Getting User...")
    #         UHelix = THelix.user(" ".join(args))
    #         Name = UHelix.display_name
    #         Type = UHelix.broadcaster_type.capitalize()
    #         PImg = UHelix.profile_image_url
    #         SHelix = UHelix.stream
    #         State = SHelix.type.upper()
    #         StreamTitle = SHelix.title
    #         CurrentViewers = SHelix.viewer_count
    #         StartTime = SHelix.started_at.replace("T"," ")[:-1]
    #         ThumbnailShot = SHelix.thumbnail_url.format(**{"width":1920, "height":1080})
    #         ThumbnailShot = requests.get(ThumbnailShot, allow_redirects=True)
    #         open("Thumb.jpg", "wb").write(ThumbnailShot.content)
    #         async with pyimgbox.Gallery(title="The Thumbnail") as gallery:
    #             Img = await gallery.upload("Thumb.jpg")
    #             ThumbnailShot = Img["image_url"]
    #         os.remove("Thumb.jpg")
    #         ThEm = discord.Embed(title = StreamTitle, description = f':red_circle: {State}', url = f'https://www.twitch.tv/{Name}',color = 0x9147FF)
    #         ThEm.set_author(name=f'{Name} ({Type})', icon_url=PImg)
    #         ThEm.set_image(url=ThumbnailShot)
    #         ThEm.add_field(name = "Live Viewers: ", value = f'{CurrentViewers:,}')
    #         ThEm.add_field(name = "Started At: ", value = StartTime)
    #         await ctx.response.send_message(embed = ThEm)
    #     except Exception as error:
    #         if error.__class__ == StreamNotFound: await SendWait(ctx, "Streamer is not currently LIVE")
    #         if error.__class__ == AttributeError: await SendWait(ctx, "User Not Found")

    # @TTwitch.command(name="clips")
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def StreamerClips(self, ctx, *args):
    #     if not args: await SendWait(ctx, "No Username"); return
    #     try:
    #         UHelix = THelix.user(" ".join(args))
    #         Name = UHelix.display_name
    #         Type = UHelix.broadcaster_type.capitalize()
    #         PImg = UHelix.profile_image_url
    #         await SendWait(ctx, ":tv: Getting Clips...")
    #         VHelix = list(UHelix.videos())
    #         if not VHelix: await SendWait(ctx, "User Has No Clips"); return
    #         VHelix = VHelix[:20]
    #         TotalClips = len(VHelix)
    #         ClipEms = []
    #         for N , Clip in enumerate(VHelix, start=1): 
    #             CEm = discord.Embed(title=f'{Clip.title} ({Clip.viewable.capitalize()})', url=Clip.url, description=Clip.description, color=0x9147FF)
    #             if Clip.thumbnail_url: CEm.set_image(url = Clip.thumbnail_url.replace("%","").format(**{"width":1920, "height":1080}))
    #             else: CEm.add_field(name = ":diamond_shape_with_a_dot_inside: Thumbnail not Found", value="\u200b", inline=False)
    #             CEm.set_author(name=f'{Name} ({Type})', icon_url=PImg)
    #             CEm.add_field(name = f'*Clip:* `[{N}/{TotalClips}]`', value="\u200b", inline=False)
    #             CEm.add_field(name = "Views: ", value=f'{Clip.view_count:,}')
    #             CEm.add_field(name = "Published On: ", value=f'{Clip.published_at.replace("T"," ")[:-1]}')
    #             ClipEms.append(CEm)
    #     except AttributeError: await SendWait(ctx, "Not Found"); return
    #     await Navigator(ctx, ClipEms)

    # @commands.group(name="twitter", invoke_without_command=True)
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def TwitterNav(self, ctx, *args):
    #     def ChCHanS(MSg):
    #         MesS = MSg.content.lower()
    #         RsT = False
    #         try:
    #             if int(MSg.content) <= 10: RsT = True
    #         except ValueError:
    #             if MesS in ["cancel", "c"]: RsT = True
    #         return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

    #     TWinput = list(args)
    #     if TWinput and TWinput[0].lower() == "search":
    #         TWinput.pop(0)
    #         if TWinput:
    #             C = 0
    #             SrchTw = []
    #             for TWuser in Twitter.search_users(TWinput, count=10):
    #                 C += 1
    #                 if C == 1: STEm = discord.Embed(title=f':mag: Search for "{" ".join(TWinput)}"', description="\u200b", color=0x0384FC)
    #                 IsVerified = ""
    #                 if TWuser.verified: IsVerified = ":ballot_box_with_check: "
    #                 STEm.add_field(name="\u200b", value=f"{C}. `@{TWuser.screen_name} / {TWuser.name}` {IsVerified}", inline=False)
    #                 SrchTw.append(TWuser)
    #             if not C: await SendWait(ctx, "Not Found :expressionless:"); return
    #             STEm.set_footer(text='Choose a number to open Twitter User Profile. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
    #             TwSent = await ctx.response.send_message(embed=STEm)
    #             try:
    #                 ResS = await self.DClient.wait_for("message", check=ChCHanS, timeout=20)
    #                 LResS = ResS.content.lower()
    #                 try:
    #                     if int(ResS.content) <= 10:
    #                         TWchoice = SrchTw[int(ResS.content) - 1]
    #                         IsVerified = ""
    #                         if TWchoice.verified: IsVerified = ":ballot_box_with_check: "
    #                         TWname = SrchTw[int(ResS.content) - 1].screen_name
    #                         await TwSent.edit(embed=discord.Embed(title=":calling: Finding...", description=f"@{TWchoice.screen_name} / {TWchoice.name} {IsVerified}", color=0x0384FC))
    #                 except ValueError:
    #                     if LResS in ["cancel", "c"]: await TwSent.edit(embed=discord.Embed(title=":x: Search Cancelled", description="\u200b", color=0x0384FC))
    #             except asyncio.TimeoutError: await TwSent.edit(embed=discord.Embed(title=":hourglass: Search Timeout...", description="\u200b", color=0x0384FC))
    #         else: await SendWait(ctx, "No search argument :woozy_face:"); return
    #     elif args: TWname = " ".join(args)
    #     else: await SendWait(ctx, "No Arguments :no_mouth:"); return
    #     try:
    #         TWprofile = Twitter.get_user(TWname)
    #         IsVerified = ""
    #         TWdesc = "\u200b"
    #         if TWprofile.verified: IsVerified = ":ballot_box_with_check: "
    #         if TWprofile.description: TWdesc = TWprofile.description
    #         TEm = discord.Embed(title=f"@{TWprofile.screen_name} / {TWprofile.name} {IsVerified}", description=TWdesc, color=0x0384FC)
    #         TEm.set_thumbnail(url=TWprofile.profile_image_url_https)
    #         if TWprofile.location: TEm.add_field( name="Location: ", value=TWprofile.location, inline=True)
    #         if TWprofile.url: TEm.add_field(name="Website: ", value=(requests.head(TWprofile.url)).headers["Location"], inline=True)
    #         TEm.add_field(name="Created: ", value=(str(TWprofile.created_at).split(" "))[0], inline=False)
    #         TEm.add_field(name="Following: ", value=f"{TWprofile.friends_count:,}", inline=True)
    #         TEm.add_field(name="Followers: ", value=f"{TWprofile.followers_count:,}", inline=True)
    #         TEm.set_footer(text="Need help navigating? zhelp navigation")
    #         TWtimeline = Twitter.user_timeline(TWname, trim_user=True, tweet_mode="extended")
    #         Twts = [TwitterbedMaker(TWprofile, IsVerified, ChTwTp(T), T, Tn, len(TWtimeline)) for Tn, T in enumerate(TWtimeline)]
    #         await Navigator(ctx, Twts, Main=True, MainBed=TEm)
    #     # except UnboundLocalError: pass
    #     except tweepy.error.TweepError: await SendWait(ctx, "Not Found :expressionless:")

    # @TwitterNav.command(name="trending")
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def TwitterTrends(self, ctx, *args):
    #     Trends = Twitter.trends_place(id=23424977)
    #     TEm = discord.Embed(title=f'Currently Trending (USA) ({Trends[0]["as_of"][:10]} {Trends[0]["as_of"][12:16]})', color=0x0384FC)
    #     for Trend in Trends[0]["trends"]:
    #         if Trend["tweet_volume"]: TEm.add_field(name=Trend["name"], value=f'{Trend["tweet_volume"]:,} Tweets', inline=False)
    #         else: TEm.add_field(name=Trend["name"], value=f"\u200b", inline=False)
    #     await ctx.response.send_message(embed=TEm)

    # @commands.command(aliases=["youtube", "yt"])
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def YoutubeGetter(self, ctx, *args):
    #     def ChCHanS(MSg):
    #         MesS = MSg.content.lower()
    #         RsT = False
    #         try:
    #             if int(MSg.content) <= 10: RsT = True
    #         except ValueError:
    #             if MesS in ["cancel", "c"]: RsT = True
    #         return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

    #     YTinput = list(args)
    #     if YTinput and YTinput[0].lower() == "search":
    #         IDorName = "ID"
    #         YTinput.pop(0)
    #         if YTinput:
    #             C = 0
    #             SrchYT = []
    #             for YTchannel in YClient.search(q=" ".join(YTinput), count=10, search_type="channel").items:
    #                 ChannelGetter = YClient.get_channel_info(channel_id=YTchannel.snippet.channelId)
    #                 C += 1
    #                 if C == 1: SYem = discord.Embed(title=f':mag: Search for "{" ".join(YTinput)}"', description="\u200b", color=0xFF0000)
    #                 if not ChannelGetter.items[0].statistics.hiddenSubscriberCount: SYem.add_field(name="\u200b", value=f"{C}. `{ChannelGetter.items[0].snippet.title} / Subs: {int(ChannelGetter.items[0].statistics.subscriberCount):,} / Videos: {int(ChannelGetter.items[0].statistics.videoCount):,}`", inline=False)
    #                 else: SYem.add_field(name="\u200b", value=f"{C}. `{ChannelGetter.items[0].snippet.title} / Videos: {int(ChannelGetter.items[0].statistics.videoCount):,}`", inline=False)
    #                 SrchYT.append(ChannelGetter)
    #             if C == 0: await SendWait(ctx, "Nothing Found :woozy_face:"); return
    #             SYem.set_footer(text='Choose a number to open Youtube Channel. "c" or "cancel" to exit search.\n\n*The Search closes automatically after 20sec of inactivity.*')
    #             YTSent = await ctx.response.send_message(embed=SYem)
    #             try:
    #                 ResS = await self.DClient.wait_for("message", check=ChCHanS, timeout=20)
    #                 LResS = ResS.content.lower()
    #                 try:
    #                     if int(ResS.content) <= 10:
    #                         YTchoice = SrchYT[int(ResS.content) - 1]
    #                         YTid = YTchoice.items[0].id
    #                         if not YTchoice.items[0].statistics.hiddenSubscriberCount: await YTSent.edit(embed=discord.Embed(title=":calling: Finding...", description=f"{YTchoice.items[0].snippet.title} / Subs: {int(YTchoice.items[0].statistics.subscriberCount):,} / Videos: {int(YTchoice.items[0].statistics.videoCount):,}", color=0xFF0000))
    #                         else: await YTSent.edit(embed=discord.Embed(title=":calling: Finding...", description=f"{YTchoice.items[0].snippet.title} / Videos: {int(YTchoice.items[0].statistics.videoCount):,}", color=0xFF0000))
    #                 except ValueError:
    #                     if LResS in["cancel", "c"]: await YTSent.edit(embed=discord.Embed(title=":x: Search Cancelled", description="\u200b", color=0xFF0000)); return
    #             except asyncio.TimeoutError: await YTSent.edit(embed=discord.Embed(title=":hourglass: Search Timeout...", description="\u200b", color=0xFF0000)); return
    #         else: await SendWait(ctx, "No search argument :woozy_face:"); return
    #     elif YTinput: IDorName = "NAME"; print("olol")
    #     else: await SendWait(ctx, "No Arguments :no_mouth:"); return
    #     Info = lambda x:YClient.get_channel_info(channel_id=x)
    #     Vids = lambda x:YClient.get_activities_by_channel(channel_id=x, count=20)
    #     if IDorName == "NAME":
    #         try:
    #             YTtempID = YClient.search(q=" ".join(YTinput), count=1, search_type="channel").items[0].snippet.channelId
    #             YTinfo, YTVids = Threader([Info, Vids], [[YTtempID]]*2)
    #         except IndexError: 
    #             await SendWait(ctx, "Nothing Found :woozy_face:"); return; print("hiter")
    #     elif IDorName == "ID": YTinfo, YTVids = Threader([Info, Vids], [[YTid]]*2)
    #     await SendWait(ctx, "Getting Channel...")
    #     YTdesc = (YTinfo.items[0].snippet.description)[:253]
    #     YEm = discord.Embed(title=YTinfo.items[0].snippet.title, description=YTdesc, url=f"https://www.youtube.com/channel/{YTinfo.items[0].id}", color=0xFF0000)
    #     YEm.add_field(name="Created on:", value=YTinfo.items[0].snippet.publishedAt[:10], inline=False)
    #     if not YTinfo.items[0].statistics.hiddenSubscriberCount: YEm.add_field(name="Subscribers:", value=f"{int(YTinfo.items[0].statistics.subscriberCount):,}", inline=False)
    #     YEm.add_field(name="Videos:", value=f"{int(YTinfo.items[0].statistics.videoCount):,}", inline=True)
    #     YEm.add_field(name="\u200b", value="\u200b", inline=True)
    #     YEm.add_field(name="Total Views:", value=f"{int(YTinfo.items[0].statistics.viewCount):,}", inline=True)
    #     YEm.set_thumbnail(url=YTinfo.items[0].snippet.thumbnails.high.url)
    #     YTEs = [YoutubebedMaker(Vid.contentDetails.upload.videoId, YTinfo.items[0], VNum, len(YTVids.items)) for VNum, Vid in enumerate(YTVids.items)]
    #     await Navigator(ctx, YTEs, Main=True, MainBed=YEm)
    async def CheckSub(self, Sub:str) -> bool:
        try:
            self.Reddit.subreddits.search_by_name(Sub, exact=True)
            (await self.Reddit.subreddit(Sub, fetch=True)).subreddit_type
        except (NotFound, Forbidden): return False
        return True

    RedditSlashes = app_commands.Group(name="reddit", description="Main Command Group for Reddit.")

    @RedditSlashes.command(name="get", description="Get a Post from a Subreddits's RISING Posts.")
    @app_commands.rename(sub="subreddit")
    @app_commands.describe(sub="Name of Subreddit")
    @app_commands.checks.cooldown(1, 2)
    async def RedditRand(self, ctx:discord.Interaction, sub:str) -> None:
        if not sub: await SendWait("No arguments :no_mouth:"); return
        args = sub[2:] if sub.startswith("r/") else sub
        await ctx.response.defer(thinking=True)
        if (await self.CheckSub(args)):
            # async with asyncReddit as Reddit:
            SubCpoS = await (await self.Reddit.subreddit(args, fetch=True)).random() # [i for i in list(Reddit.subreddit(args).hot()) if not i.stickied]
            # print(len(list(SubCpoS)), SubCpoS)
            if not SubCpoS: await ctx.followup.send("No Posts Found :expressionless:")
            # SubCpoS = random.choice(Post)
            Nsfwcheck=ctx.channel.is_nsfw()
            await ctx.followup.send(embed=RedditbedMaker(SubCpoS, args, Nsfwcheck))
        else: await ctx.followup.send("Sub doesn't exist or private :expressionless:")

    async def RedditNav(self, ctx:discord.Interaction, sub:str, ctp:str) -> None:
        async def rdtEmBldr(pst):
            Embeder = lambda i,*x: [RedditbedMaker(P, sub, Nsfchannel=Nsfwcheck, Type="S", PostNum=i+PNum, TotalPosts=TotalPosts) for PNum, P in enumerate(x)]
            SubCpoS = [SuTPos async for SuTPos in pst if not SuTPos.stickied]
            TotalPosts = len(SubCpoS)
            if TotalPosts == 0: return []
            Nsfwcheck=ctx.channel.is_nsfw
            Crsd = np.array_split(SubCpoS, len(SubCpoS)//2)
            Crsd = [np.insert(i, 0, v*2) for v,i in enumerate(Crsd)]
            Thread = Threader([Embeder]*(len(SubCpoS)//2), Crsd)
            if(Thread == False):  return []
            return sum(Thread, [])
            
        async def updateNav(srt:str):
            Post = await self.Reddit.subreddit(sub, fetch=True)
            match srt:
                case "Top All Time":
                    Post = Post.top("all", limit=50)
                case "Top This Month":
                    Post = Post.top("month", limit=50)
                case "Top Today":
                    Post = Post.top("day", limit=50)
                case "Rising":
                    Post = Post.rising(limit=50)
                case "Hot":
                    Post = Post.hot(limit=50)
                case "New":
                    Post = Post.new(limit=50)
            return await rdtEmBldr(Post)
        
        if not (await self.CheckSub(sub)) and not ctp == "c2": await SendWait(ctx, "Sub doesn't exist or private :expressionless:"); return
        await SortedNav(updateNav, ["Top All Time", "Top This Month", "Top Today", "Rising", "Hot", "New"], 
                        ["🌍", "🗓️", "📅", "📈", "🔥", "📝"], ctx).autoRun()
        # await Navigator(ctx, PostEms).autoRun()

    @RedditSlashes.command(name="surf", description="Navigate a Subreddit on Discord.")
    @app_commands.rename(sub="subreddit")
    @app_commands.describe(sub="Name of Subreddit")
    @app_commands.checks.cooldown(1, 4)
    async def singleSubNav(self, ctx:discord.Interaction, sub:str) -> None:
        if not sub: await SendWait(ctx, "No arguments :no_mouth:")
        args = sub[2:] if sub.startswith("r/") else sub
        await ctx.response.defer(thinking=True)
        await self.RedditNav(ctx, args, "c1")

    @app_commands.command(name="redditor", description="View a Redditors Profile.")
    @app_commands.rename(rdtr="redditor")
    @app_commands.describe(rdtr="Name of Redditor")
    @app_commands.checks.cooldown(1, 2)
    async def GetRedditor(self, ctx:discord.Interaction, rdtr:str) -> None:
        if not rdtr: await SendWait(ctx, "No arguments :no_mouth:"); return
        args = rdtr[2:] if rdtr.startswith("u/") else rdtr
        await ctx.response.defer(thinking=True)
        try:
            # async with asyncReddit as Reddit:
            User = await self.Reddit.redditor(args, fetch=True)
            UEm = discord.Embed(title=f"u/{User.name}", description=User.subreddit["public_description"], color=0x8B0000)
            UEm.add_field(name=f"{(User.link_karma + User.awarder_karma + User.awardee_karma + User.comment_karma):,} karma **·** {(datetime.datetime.now() - datetime.datetime.fromtimestamp(User.created_utc)).days} days", value="\u200b", inline=False)
            UEm.add_field(name=f'Trophies: `{", ".join([trophy.name for trophy in await User.trophies()])}`', value="\u200b", inline=False)
            UEm.set_thumbnail(url=User.icon_img)
            SubCpoS = [SuTPos async for SuTPos in User.submissions.new() if not SuTPos.stickied]
            TotalPosts = len(SubCpoS)
            if TotalPosts == 0: await SendWait(ctx, "No posts :no_mouth:"); return
            Name = args
            Nsfwcheck = ctx.channel.is_nsfw()
            PostEms = [RedditbedMaker(P, Name, Nsfchannel=Nsfwcheck, Type="S", PostNum=PNum, TotalPosts=TotalPosts) for PNum, P in enumerate(SubCpoS)]
            await Navigator(ctx, PostEms, Main=True, MainBed=UEm).autoRun()
        except NotFound: await SendWait(ctx, "Redditor Not Found :no_mouth:")

    #aliases=["mltr"]
    # @commands.check(ChPatreonT2)
    # @commands.check(ChMaxMultireddits)        
    MultiredditSlashes = app_commands.Group(name="multireddit", description="Main Command Group for MultiReddit.")

    @MultiredditSlashes.command(name="surf", description="Navigate a Multireddit on Discord.")
    @app_commands.rename(mltr="multireddit")
    @app_commands.describe(mltr="Name of Multireddit")
    @app_commands.checks.cooldown(1, 4)
    async def GetMultis(self, ctx:discord.Interaction, mltr:str) -> None:
        if not mltr: await SendWait(ctx, "You forgot to add a Multireddit name"); return
        await ctx.response.defer(thinking=True)
        if not Rdt.count_documents({"IDd": ctx.user.id}) > 0: await SendWait(ctx, "No Multireddits Found"); return
        User = Rdt.find({"IDd": ctx.user.id})[0]
        if mltr in User and mltr not in ["IDd","_id"]:
            Subreddits = "+".join(User[mltr])
            await self.RedditNav(ctx, Subreddits, "c2")
        else: await SendWait(ctx, f"That Multireddit ({mltr}) doesn't exist")

    # @commands.check(ChPatreonT2)
    @MultiredditSlashes.command(name="list", description="Lists your Multireddit and Contained Subreddits.")
    @app_commands.checks.cooldown(1, 2)
    async def ListMultis(self, ctx:discord.Interaction):
        await ctx.response.defer(thinking=True)
        if not Rdt.count_documents({"IDd": ctx.user.id}): await SendWait(ctx, "No Multireddits Found"); return
        User = Rdt.find({"IDd": ctx.user.id})[0]
        MEm = discord.Embed(title=f"{ctx.user.display_name}'s MultiReddits", color=0x8B0000)
        for Multireddit in User:
            if Multireddit not in ["IDd", "_id"]: MEm.add_field(name=Multireddit, value=f'`{", ".join(User[Multireddit])}`')
        await ctx.followup.send(embed=MEm)

    # @commands.check(ChPatreonT2)
    # @commands.check(ChMaxMultireddits)
    @MultiredditSlashes.command(name="create", description="Create a New Multireddit.")
    @app_commands.rename(mltr="multireddit")
    @app_commands.describe(mltr="Name of Multireddit")
    @app_commands.checks.cooldown(1, 2)
    async def CreateMulti(self, ctx:discord.Interaction, mltr:str) -> None:
        if not mltr: await SendWait(ctx, "No Arguments"); return
        await ctx.response.defer(thinking=True)
        # ArgumentHandle = list(args)
        TierApplicable = {"Tier 2 Super": 1, "Tier 3 Legend": 2, "Tier 4 Ultimate": 4}
        # TierLimit = TierApplicable[GetPatreonTier(ctx.author.id)]
        TierLimit = 4
        if not Rdt.count_documents({"IDd": ctx.user.id}):
            Rdt.insert_one({"IDd": ctx.user.id, mltr: []})
            await SendWait(ctx, f"Added the Multireddit ({mltr}), you can now add and remove subreddits from it.")  
            return
        User = Rdt.find({"IDd": ctx.user.id})[0]
        if len(User) < TierLimit:
            #- for Multireddit in User:
            if mltr in User: await SendWait(ctx, f"Multireddit ({mltr}) Already Exists"); return
            else: Rdt.update_one(User, {"$set": {mltr: []}})
            await SendWait(ctx, f"Added the Multireddit ({mltr}), you can now add and remove subreddits from it.")
        else: await SendWait(ctx, "You already have the maximum amount of Multireddits. You can use 'zmultireddit' to see your multireddits or check 'zpatreon' to know more about limits") 

    # @commands.check(ChPatreonT2)  aliases=["del"]
    @MultiredditSlashes.command(name="delete", description="Delete an Existing Multireddit.")
    @app_commands.rename(mltr="multireddit")
    @app_commands.describe(mltr="Name of Multireddit")
    @app_commands.checks.cooldown(1, 2)
    async def DeleteMulti(self, ctx:discord.Interaction, mltr:str) -> None:
        if not mltr: await SendWait(ctx, "No Arguments"); return
        await ctx.response.defer(thinking=True)
        # ArgumentHandle = list(args)
        if not Rdt.count_documents({"IDd": ctx.user.id}): await SendWait(ctx, "You don't have any Multireddits"); return
        User = Rdt.find({"IDd": ctx.user.id})[0]
        Multis = len(User) - 2
        #- for Multireddit in User:
        if mltr in User and mltr not in ["_id", "IDd"]:
            if Multis == 1: Rdt.delete_one({"IDd": ctx.user.id})
            else: Rdt.update_one(User, {"$unset": {mltr: ""}})
            await SendWait(ctx, f"Deleted the Multireddit ({mltr}).")
            return
        else: await SendWait(ctx, "That Multireddit Doesn't Exist"); return

    # @commands.check(ChPatreonT2)
    # @commands.check(ChMaxMultireddits)
    @MultiredditSlashes.command(name="add", description="Add Subreddits to Multireddit.")
    @app_commands.rename(mltr="multireddit")
    @app_commands.describe(mltr="Name of Multireddit")
    @app_commands.rename(subs="subreddits")
    @app_commands.describe(subs="Names of Subreddits (Spaced)")
    @app_commands.checks.cooldown(1, 2)
    async def AddMulti(self, ctx:discord.Interaction, mltr:str, subs:str) -> None:
        if not mltr or not subs: await SendWait(ctx, "No Arguments"); return
        await ctx.response.defer(thinking=True)
        # Multi, Subs = args[0], list(args[1:])
        subs = subs.split(" ")
        User = Rdt.find({"IDd": ctx.user.id})[0]
        Added, NotAdded = [], []
        if mltr in User and mltr not in ["IDd", "_id"]:
            for Sub in subs:
                Sub = Sub[2:] if Sub.startswith("r/") else Sub
                if Sub not in User[mltr] and Sub not in Added:
                    if not (await self.CheckSub(Sub)): NotAdded.append(Sub); continue
                    Added.append(Sub) 
                else: NotAdded.append(Sub)
            if Added:
                # print({"$set": {mltr: User[mltr]+Added}})
                Rdt.update_one(User, {"$set": {mltr: User[mltr]+Added}})
                await SendWait(ctx, f'Added the following Subreddit(s) to Multireddit: `{", ".join(Added)}`')
            if NotAdded: await SendWait(ctx, f"Following Subreddit(s) didn't exist, private, or already added: `{', '.join(NotAdded)}`")
        else: await SendWait(ctx, f"That Multireddit ({mltr}) does not exist. Check if the name is right or create it.")

    # @commands.check(ChPatreonT2)
    # @commands.check(ChMaxMultireddits) aliases=["rem"], 
    @MultiredditSlashes.command(name="remove", description="Remove Subreddits from Multireddit.")
    @app_commands.rename(mltr="multireddit")
    @app_commands.describe(mltr="Name of Multireddit")
    @app_commands.rename(subs="subreddits")
    @app_commands.describe(subs="Names of Subreddits (Spaced)")
    @app_commands.checks.cooldown(1, 2)
    async def RemMulti(self, ctx:discord.Interaction, mltr:str, subs:str) -> None:
        if not mltr or not subs: await SendWait(ctx, "No Arguments"); return
        await ctx.response.defer(thinking=True)
        # Multi, Subs = args[0], list(args[1:])
        subs = subs.split(" ")
        Removed, NotRemoved = [], []
        if not Rdt.count_documents({"IDd": ctx.user.id}): await SendWait(ctx, "You don't have any Multireddits"); return
        User = Rdt.find({"IDd": ctx.user.id})[0]
        if mltr in User and mltr not in ["IDd","_id"]:
            Remover = User[mltr]
            for Sub in subs:
                Sub = Sub[2:] if Sub.startswith("r/") else Sub
                if Sub in Remover and Sub not in Removed:
                    if not (await self.CheckSub(Sub)): NotRemoved.append(Sub); continue
                    Remover.remove(Sub)
                    Removed.append(Sub)
            
            if Removed: 
                # print({"$set": {mltr: Remover}})
                Rdt.update_one(User, {"$set": {mltr: Remover}})
                await SendWait(ctx, f'Removed the following Subreddit(s) from Multireddit: `{", ".join(Removed)}`')
            if NotRemoved: await SendWait(ctx, f"Following Subreddit(s) didn't exist in Multireddit: `{', '.join(NotRemoved)}`")
        else: await SendWait(ctx, f"That Multireddit ({mltr}) does not exist. Check if the name is right or create it.")
            
    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")


async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(Socials(DClient))