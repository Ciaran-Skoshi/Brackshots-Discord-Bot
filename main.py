import discord
from discord.ext import commands
import subprocess
import json
import re
from datetime import datetime
import game #game.py

gameMaster = game.GameMaster()
games = []
counter = 0

with open("jayson.json", "r") as f:
    j = json.loads(f.read())
    token = j["token"]
    serverID = j["serverID"]

#Makes sure the status.txt is set correctly
with open("minecraftServer/status.json", "w") as f:
    f.write(json.dumps(False))

class Client(commands.Bot):
    async def on_ready(self):
        global serverID
        print(f"Logged on as {self.user}")
        

        #Forces commands to update on the main server
        try:
            guild = discord.Object(id=serverID)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} command(s) to guild {guild.id}")
        except Exception as e:
            print(f"Error syncing command(s): {e}")

    async def on_message(self, message):
        global games
        thisGame = None
        if (message.author == self.user) or (len(games) == 0):
            return
        if client.user in message.mentions:
            for game in games:
                if game.player == message.author:
                    thisGame = game
            
            if thisGame == None:
                return
            #Appends the message content with the bot ping and any white space before and after it removed
            thisGame.filledInWords.append(re.sub(r"\s*<@1437276201386377298>\s*", "", message.content))
            
            if len(thisGame.filledInWords) < len(thisGame.fillInWords):
                await message.channel.send(f"Give me a(n) {thisGame.getFillInWord()} <@{message.author.id}>", allowed_mentions=discord.AllowedMentions(users=True))
        
        if len(thisGame.filledInWords) == len(thisGame.fillInWords):
            await message.channel.send(thisGame.showMadLib())
            games.remove(thisGame)
    

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=serverID)

GUILD_IDS = [discord.Object(id=serverID), discord.Object(id=1437275679371821180)]


@client.tree.command(name="test-command", description="Command that does whatever I need it to do", guilds=GUILD_IDS)
async def testCommand(interaction: discord.Interaction):
    await interaction.response.send_message("Nothing to test")

@client.tree.command(name="how-to-play-mad-libs", description="Tells how to use this bot to play a Mad Lib!", guild=GUILD_ID)
async def howToMadLib(interaction: discord.Interaction):
    embed = discord.Embed(title="How to play", colour=discord.Colour.blue())
    embed.add_field(name="How to start a Mad Lib:", value='To start a Mad Lib simply run the "play-mad-lib" command and select a Mad Lib from the dropdown menu (Example Mad Lib is a very short one and good to get an idea of how a Mad Lib works)', inline=False)
    embed.add_field(name="How to play a Mad Lib:", value="Once you have selected a Mad Lib all you need to do is reply to the bot's message (Making sure to ping it or else it will not work) with the word you want to use, keep doing this until the bot spits out your glorious work of writing")
    await interaction.response.send_message(embed=embed)

class Menu(discord.ui.Select):
    def __init__(self):
        options = []
        for madLib in gameMaster.madLibsFiles:
            options.append(discord.SelectOption(label=madLib.name.removesuffix(".txt")))
        super().__init__(placeholder="Please select a Mad Lib", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        global game, games
        newGame = game.Game(interaction.user)
        x = 0
        for madLib in gameMaster.madLibsFiles:
            if madLib.name.removesuffix(".txt") == self.values[0]:
                newGame.selectMadLib(gameMaster.madLibsFiles[x])
                newGame.getFillInWords()
                #Todo: Make this ping the user who started the game
                await interaction.response.send_message(f"Give me a(n) {newGame.getFillInWord()}") #@<{interaction.user.id}> allowed_mentions=discord.AllowedMentions(users=True)
                games.append(newGame)
                return
            x += 1


class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())

@client.tree.command(name="play-mad-lib", description="Play a Mad Lib!", guild=GUILD_ID)
async def playMadLib(interaction: discord.Interaction):
    await interaction.response.send_message(view=MenuView())

@client.tree.command(name="how-to-join-minecraft", description="Instructions on how to join The Brackshots Minecraft Server", guild=GUILD_ID)
async def howToJoinMinecraft(interaction: discord.Interaction):
    embed = discord.Embed(title="How to join The Brackshots Minecraft Server", colour=discord.Colour.green())
    #embed.set_thumbnail
    embed.add_field(name="Direct IP:", value='You should hopfully be able to join the Minecraft server with the IP of "effect-exposed.gl.joinmc.link" however if this does not work you will have to join through', inline=False)
    embed.add_field(name="LogMeIn Hamachi:", value='If you are using LogMeIn Hamachi, you can join the Minecraft server by joining the Hamachi network and copying the IPv4 address of the host, if you need assistance, @ or DM Skoshi')
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="start-minecraft-server", description="Starts the Brackshots Minecraft Server", guild=GUILD_ID)
async def startMinecraftServer(interaction: discord.Interaction):
    with open("minecraftServer/status.json", "r") as f:
        running = json.loads(f.read())
        if not running:
            subprocess.Popen(["python3 serverMC.py"], cwd="minecraftServer", shell=True, stdin=subprocess.PIPE, stdout= subprocess.PIPE)
            await interaction.response.send_message("Starting Server")
        else:
            await interaction.response.send_message("Server already on")

@client.tree.command(name="most-used-word-of-the-day", description="Shows the top 5 used words of any particular day in the channel you run this command in", guild=GUILD_ID)
async def mostUsedWordOfDay(interaction: discord.Interaction, year: int, month :int, day :int):
    try:
        selectedDate = datetime(year, month, day)
    except:
        print(f"Bad date given: {year}/{month}/{day}")
        await interaction.response.send_message("Error: Invaild date given")
        return

    dayBefore = datetime.fromtimestamp(selectedDate.timestamp() - 86400)
    dayAfter = datetime.fromtimestamp(selectedDate.timestamp() + 86400)
    
    
    wordCount :dict = {}
    messages = interaction.channel.history(limit=10000, after=dayBefore, before=dayAfter)
    
    async for msg in messages:
        words = msg.content.split()
        for word in words:
            
            if "http" in word:
                wordCount[word] = wordCount.get(word, 0) + 1
                continue

            if word.startswith("<"):
                wordCount[word] = wordCount.get(word, 0) + 1
                continue

            #get rid of , . ' ; 
            cleanWord = re.sub(r'[^\w\s]', '', word)
            cleanWord = cleanWord.lower()
            wordCount[cleanWord] = wordCount.get(cleanWord, 0) + 1
    
    res = {k: v for k, v in sorted(wordCount.items(), key=lambda item: (item[1], item[0]), reverse=True)}
    
    highestKeys = []
    i = 0
    for k, v in res.items():
        highestKeys.append(k)
        i += 1
        if i == 5:
            break
    #<t:1765454400:s>
    message = f"Top five used words on <t:{int(selectedDate.timestamp())}:s> are:\n"
    for j in highestKeys:
        message += f"{j}: {res[j]}\n"
    await interaction.channel.send(message)

@client.tree.command(name="increment-counter", description="Increment the super cool and awesome counter, because you and cool and nice", guild=GUILD_ID)
async def incrementCounter(interaction: discord.Interaction):
    global counter
    counter += 1
    await interaction.response.send_message(f"Counter is now {counter}!")

@client.tree.command(name="decrement-counter", description="Decrement the super cool and awesome counter, because you are evil and fucked up", guild=GUILD_ID)
async def incrementCounter(interaction: discord.Interaction):
    global counter
    counter -= 1
    await interaction.response.send_message(f"Counter is now {counter}!")


client.run(token)

