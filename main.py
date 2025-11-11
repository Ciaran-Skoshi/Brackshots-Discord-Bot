import os
import discord
from discord.ext import commands
from discord import app_commands
import game #game.py

game = game.Game()
isPlaying = False

class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

        try:
            guild = discord.Object(id=1437275679371821180)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} command(s) to guild {guild.id}")
        except Exception as e:
            print(f"Error syncing command(s): {e}")

    async def on_message(self, message):
        global isPlaying
        if message.author == self.user:
            return
        if isPlaying:
            if client.user in message.mentions:
                game.filledInWords.append(message.content)
                print(f"Current Filled In Words: ", game.filledInWords)
                if len(game.filledInWords) < len(game.fillInWords):
                    await message.channel.send(f"Give me a(n) {game.getFillInWord()}")
        print(f"Fill in words: {game.fillInWords}, Filled in words: {game.filledInWords}")
        print(f"Message: {message.content}, isPlaying: {isPlaying}")
        if len(game.filledInWords) == len(game.fillInWords) and isPlaying:
            await message.channel.send(game.showMadLib())
            game.reset()
            isPlaying = False
    

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)


GUILD_ID = discord.Object(id=1437275679371821180)

@client.tree.command(name="help", description="Show how to use this bot to play a Mad Lib!", guild=GUILD_ID)
async def howToMadLib(interaction: discord.Interaction):
    embed = discord.Embed(title="How to play", description="TODO: Write description", colour=discord.Colour.blue())
    await interaction.response.send_message(embed=embed)

class Menu(discord.ui.Select):
    def __init__(self):
        options = []
        for madLib in game.madLibsFiles:
            options.append(discord.SelectOption(label=madLib.name.removesuffix(".txt")))
        super().__init__(placeholder="Please select a Mad Lib", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        global isPlaying
        x = 0
        for madLib in game.madLibsFiles:
            if madLib.name.removesuffix(".txt") == self.values[0]:
                #await interaction.response.send_message(f"You picked {self.values[0]}")
                game.selectMadLib(x)
                game.getFillInWords()
                await interaction.response.send_message(f"Give me a(n) {game.getFillInWord()}")
                isPlaying = True
                return
            x += 1


class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())

@client.tree.command(name="play", description="Play a Mad Lib!", guild=GUILD_ID)
async def playMadLib(interaction: discord.Interaction):
    global isPlaying
    if isPlaying:
        await interaction.response.send_message(f"Unable to start game: Someone else is playing")
    else:
        await interaction.response.send_message(view=MenuView())

with open("token.txt", "r") as f:
    token = f.read()
    #print(token)

client.run(token)