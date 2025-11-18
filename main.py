import discord
from discord.ext import commands
import subprocess
import game #game.py

gameMaster = game.GameMaster()
games = []

class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

        #Forces commands to update on the testing server
        try:
            guild = discord.Object(id=1437275679371821180)
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
            
            thisGame.filledInWords.append(message.content)
            
            if len(thisGame.filledInWords) < len(thisGame.fillInWords):
                await message.channel.send(f"Give me a(n) {thisGame.getFillInWord()} <@{message.author.id}>", allowed_mentions=discord.AllowedMentions(users=True))
        
        if len(thisGame.filledInWords) == len(thisGame.fillInWords):
            await message.channel.send(thisGame.showMadLib())
            games.remove(thisGame)
    

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)


GUILD_ID = discord.Object(id=1437275679371821180)

@client.tree.command(name="test-command", description="Shows the author of the interaction", guild=GUILD_ID)
async def testCommand(interaction: discord.Interaction):
    await interaction.response.send_message(f"Interaction Author = {interaction.user}")

@client.tree.command(name="mad-lib-help", description="Show how to use this bot to play a Mad Lib!", guild=GUILD_ID)
async def howToMadLib(interaction: discord.Interaction):
    embed = discord.Embed(title="How to play", description="TODO: Write description", colour=discord.Colour.blue())
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
    with open("minecraftServer/status.txt", "r") as f:
        if f.read() == "False":
            subprocess.Popen(["python3 serverMC.py"], cwd="minecraftServer", shell=True, stdin=subprocess.PIPE, stdout= subprocess.PIPE)
            await interaction.response.send_message("Starting Server")
        else:
            await interaction.response.send_message("Server already on")
    

#Makes sure the status.txt is set correctly
with open("minecraftServer/status.txt", "w") as f:
    f.write("False")

with open("token.txt", "r") as f:
    token = f.read()

client.run(token)

