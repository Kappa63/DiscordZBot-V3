import discord
from discord import app_commands
from discord.ext import commands
import requests
from typing import Optional
from Customs.Functions import SendWait
from PIL import Image
import deeppyer
import os
import qrcode
import cv2
from CBot import DClient as CBotDClient


class Images(commands.Cog):
    def __init__(self, DClient:CBotDClient) -> None:
        self.DClient = DClient

    @app_commands.command(name="cat", description="For All the Cat Lovers.")
    @app_commands.checks.cooldown(1, 1)
    async def RandomCat(self, ctx:discord.Interaction) -> None:
        CatGot = requests.get("https://cataas.com/cat", headers={"Accept": "application/json"}, timeout=5).json()
        CEm = discord.Embed(title="Meow", color=0xA3D7C1)
        CEm.set_image(url=f'https://cataas.com/cat/{CatGot["_id"]}')
        await ctx.response.send_message(embed=CEm)

    @app_commands.command(name="doggo", description="For All the Dog Lovers.")
    @app_commands.checks.cooldown(1, 1)
    async def RandomDoggo(self, ctx:discord.Interaction) -> None:
        DoggoGot = requests.get("https://random.dog/woof.json", headers={"Accept": "application/json"}).json()
        DEm = discord.Embed(title="Woof Woof", color=0xFF3326)
        DEm.set_image(url=DoggoGot["url"])
        await ctx.response.send_message(embed=DEm)

    @app_commands.command(name="thispersondoesnotexist", description="Just an Image of Someone That Does Not Exist.")
    @app_commands.checks.cooldown(1, 1)
    async def GetAnImaginedPerson(self, ctx:discord.Interaction) -> None:
        PEm = discord.Embed(title="This Person Does NOT Exist.", color=0x753684)
        GetTpde = requests.get("https://thispersondoesnotexist.com", allow_redirects=True)
        This = open("Tpde.png", "wb").write(GetTpde.content)
        TpdeImg = discord.File("Tpde.png")
        PEm.set_image(url="attachment://Tpde.png")
        await ctx.response.send_message(file=TpdeImg, embed=PEm)
        os.remove("Tpde.png")

    @app_commands.command(name="fox", description="For All the Fox Lovers.")
    @app_commands.checks.cooldown(1, 1)
    async def RandomFox(self, ctx:discord.Interaction) -> None:
        FoxGot = requests.get("https://randomfox.ca/floof/", headers={"Accept": "application/json"}).json()
        FEm = discord.Embed(title="What does the fox say?", color=0x9DAA45)
        FEm.set_image(url=FoxGot["image"])
        await ctx.response.send_message(embed=FEm)

    @app_commands.command(name="food", description="For All the Hungry Folk.")
    @app_commands.checks.cooldown(1, 1)
    async def RandomDishes(self, ctx:discord.Interaction) -> None:
        Hungry = requests.get("https://foodish-api.com/api/", headers={"Accept": "application/json"}).json()
        FEm = discord.Embed(title="Hungry?", color=0xDE8761)
        FEm.set_image(url=Hungry["image"])
        await ctx.response.send_message(embed=FEm)

    # @commands.command(name="pdf")
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def PDFreader(self, ctx, *args):
    #     def ChCHEmFN(MSg):
    #         MesS = MSg.content.lower()
    #         RsT = False
    #         try:
    #             if int(MSg.content): RsT = True
    #         except ValueError:
    #             if MesS in ["cancel", "c"]: RsT = True
    #         return MSg.guild.id == ctx.guild.id and MSg.channel.id == ctx.channel.id and RsT

    #     if args and ctx.message.attachments: await SendWait(ctx, "No or too many attachments :woozy_face:"); return
    #     PDFattach = []
    #     if args: PDFattach.append("".join(args))
    #     if ctx.message.attachments:
    #         for AtT in ctx.message.attachments: PDFattach.append(AtT.url)
    #     GetPDF = PDFattach[0]
    #     try:
    #         ChPDF = requests.head(GetPDF).headers.get("content-type").split("/")[1]
    #         if ChPDF != "pdf": await SendWait(ctx, "Not a PDF :woozy_face:"); return
    #         RanLetters = "ioewsahkzcldnpq"
    #         PDFname = "".join((random.choice(RanLetters) for i in range(10)))
    #         await SendWait(ctx, ":printer: Converting...")
    #         PDFcontent = requests.get(GetPDF, allow_redirects=True)
    #         open(f"{PDFname}.pdf", "wb").write(PDFcontent.content)
    #         PDFimages = convert_from_path(f"{PDFname}.pdf", 500, last_page=40)
    #         PDFcnvrt = []
    #         PageNum = 1
    #         TotalPages = len(PDFimages)
    #         Sub = []
    #         async with pyimgbox.Gallery(title=PDFname) as gallery:
    #             for i in PDFimages:
    #                 i.save(f"{PDFname}.jpg", "JPEG")
    #                 Sub.append(await gallery.upload(f"{PDFname}.jpg"))

    #         for Up in Sub:
    #             PEm = discord.Embed(title="PDF Viewer", description=f"**`{PageNum}/{TotalPages}`**")
    #             PEm.set_image(url=Up["image_url"])
    #             PDFcnvrt.append(PEm)
    #             PageNum += 1
    #         await Navigator(ctx, PDFcnvrt)
    #     except requests.exceptions.MissingSchema: await SendWait(ctx, "Not a PDF :woozy_face:")

    @app_commands.command(name="deepfry", description="Deepfry an Image Attached, Replied, or URL.")
    @app_commands.rename(URL="url")
    @app_commands.describe(URL="URL of Image")
    @app_commands.rename(img="image")
    @app_commands.describe(img="Attachment of Image")
    @app_commands.checks.cooldown(1, 2)
    async def ImageFrier(self, ctx:discord.Interaction, *, URL:Optional[str]=None, img:Optional[discord.Attachment]=None) -> None:
        if not URL and not img: await SendWait(ctx, "No image(s) or link(s) were attached :woozy_face:"); return 
        Attached = []
        if URL:
            URLargs = list(URL.split(" "))
            try:
                for url in URLargs: Attached.append(url)
            except TypeError: pass
        elif img:
            Attached.append(img)
        # elif(ctx.message.attachments):
        #     for AtT in ctx.message.attachments: 
        #         if(AtT.url not in Attached): 
        #             Attached.append(AtT.url)
        # elif (ctx.message.reference.resolved.attachments if ctx.message.type == discord.MessageType.reply else False):
        #     for AtT in ctx.message.reference.resolved.attachments: 
        #         if(AtT.url not in Attached): Attached.append(AtT.url)
        Files = []
        C = 0
        for File in Attached:
            try:
                if requests.head(File).headers.get("content-type").split("/")[0] == "image":
                    C += 1
                    GetURLimg = requests.get(File, allow_redirects=True)
                    open("NsRndo.jpg", "wb").write(GetURLimg.content)
                    Img = Image.open("NsRndo.jpg")
                    Img = await deeppyer.deepfry(Img, flares=False)
                    Img.save("NsRndo.jpg")
                    Files.append(discord.File("NsRndo.jpg"))
                    await ctx.response.send_message(files=Files)
                    Files.pop(0)
                    os.remove("NsRndo.jpg")
                else: await SendWait(ctx, f"File({C}) isnt a valid image type :sweat:")
            except requests.exceptions.MissingSchema: pass

    # @ImageFrier.command(name="profile")
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def ProfileFrier(self, ctx):
    #     if ctx.message.mentions: Profile = str((ctx.message.mentions[0]).avatar_url)
    #     else: Profile = str(ctx.author.avatar_url)
    #     try:
    #         Files = []
    #         C = 0
    #         if requests.head(Profile).headers.get("content-type").split("/")[0] == "image":
    #             C += 1
    #             GetURLimg = requests.get(Profile, allow_redirects=True)
    #             open("NsRndo.jpg", "wb").write(GetURLimg.content)
    #             Img = Image.open("NsRndo.jpg")
    #             Img = await deeppyer.deepfry(Img, flares=False)
    #             Img.save("NsRndo.jpg")
    #             Files.append(discord.File("NsRndo.jpg"))
    #             await ctx.response.send_message(files=Files)
    #             Files.pop(0)
    #             os.remove("NsRndo.jpg")
    #         else: await SendWait(ctx, f"File({C}) isnt a valid image type :sweat:")
    #     except requests.exceptions.MissingSchema: pass

    QrCodeSlashes = app_commands.Group(name = "qrcode", description="Main Command Group for QrCode.")

    @QrCodeSlashes.command(name="create", description="Text/Image to QrCode.")
    @app_commands.rename(txt="text")
    @app_commands.describe(txt="Text to Convert to QrCode")
    @app_commands.rename(img="image")
    @app_commands.describe(img="Attachment of QrCode Image")
    @app_commands.checks.cooldown(1, 2)
    async def QRmake(self, ctx:discord.Interaction, txt:Optional[str], img:Optional[discord.Attachment]) -> None:
        # and not (ctx.message.reference.resolved.attachments if ctx.message.type == discord.MessageType.reply else False)
        if not txt and not img: await SendWait(ctx, "Nothing to QR"); return
        Stuff = []
        Files = []
        if txt: Stuff.append(txt)
        elif img: Stuff.append(img)
        # elif (ctx.message.reference.resolved.attachments if ctx.message.type == discord.MessageType.reply else False): 
        #     for AtT in ctx.message.reference.resolved.attachments: 
        #         if(AtT.url not in Stuff): Stuff.append(AtT.url)
        for ToQR in Stuff:
            QRcode = qrcode.make(ToQR)
            QRcode.save("QR.png")
            Files.append(discord.File("QR.png"))
            await ctx.response.send_message(files=Files)
            os.remove("QR.png")

    @QrCodeSlashes.command(name="read", description="QrCode URL/Image to Text/Image.")
    @app_commands.rename(URL="url")
    @app_commands.describe(URL="URL of QrCode Image")
    @app_commands.rename(img="image")
    @app_commands.describe(img="Attachment of QrCode Image")
    @app_commands.checks.cooldown(1, 2)
    async def QRread(self, ctx:discord.Interaction, URL:Optional[str], img:Optional[discord.Attachment]) -> None:
        # or ctx.message.attachments or (ctx.message.reference.resolved.attachments if ctx.message.type == discord.MessageType.reply else False)
        if URL or img:
            Attached = []
            if URL:
                URLargs = list(URL.split(" "))
                try:
                    for url in URLargs: Attached.append(url)
                except TypeError: pass
            elif(img):
                Attached.append(img)
            # elif ctx.message.attachments:
            #     for AtT in ctx.message.attachments: 
            #         if(AtT.url not in Attached): Attached.append(AtT.url)
            # elif(ctx.message.reference.resolved.attachments if ctx.message.type == discord.MessageType.reply else False):
            #     for AtT in ctx.message.reference.resolved.attachments: 
            #         if(AtT.url not in Attached): Attached.append(AtT.url)
            C = 0
            for File in Attached:
                try:
                    if requests.head(File).headers.get("content-type").split("/")[0] == "image":
                        C += 1
                        GetURLimg = requests.get(File, allow_redirects=True)
                        open("QrStf.png", "wb").write(GetURLimg.content)
                        Data = cv2.QRCodeDetector().detectAndDecode(cv2.imread("QrStf.png"))[0]
                        # try:
                            # requests.get(Data)
                        # await ctx.response.send_message(Data)
                        await SendWait(ctx, Data)
                        os.remove("QrStf.png")
                    else: await SendWait(ctx, f"File({C}) doesnt contain a qrcode :sweat:")
                except requests.exceptions.MissingSchema: pass
        else: await SendWait(ctx, "No image(s) or link(s) were attached :woozy_face:")

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")

async def setup(DClient:CBotDClient) -> None:
    await DClient.add_cog(Images(DClient))
