import discord
from discord.ext import commands
import subprocess
import json

MINECRAFT_ROLE_ID = 1441513943268065331

with open("config.json", "r") as f:
    j = json.loads(f.read())
    TOKEN = j["TOKEN"]
    SERVER_ID = j["SERVER_ID"]

# Makes sure the status.txt is set correctly
with open("minecraftServer/status.json", "w") as f:
    f.write(json.dumps(False))

class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}")
        # Forces commands to update on the main server
        try:
            guild = discord.Object(id=SERVER_ID)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} command(s) to guild {guild.id}")
        except Exception as e:
            print(f"Error syncing command(s): {e}")
        

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
client = Client(command_prefix="!", intents=intents)

GUILD = discord.Object(id=SERVER_ID)

GUILDS = [discord.Object(id=SERVER_ID), discord.Object(id=1437275679371821180)]

@client.tree.command(name="how-to-join-minecraft", description="Instructions on how to join The Brackshots Minecraft Server", guild=GUILD)
@commands.has_any_role(MINECRAFT_ROLE_ID)
async def howToJoinMinecraft(interaction: discord.Interaction):
    embed = discord.Embed(title="How to join The Brackshots Minecraft Server", colour=discord.Colour.green())
    #embed.set_thumbnail
    embed.add_field(name="Direct IP:", value='You should hopefully be able to join the Minecraft server with the IP of "effect-exposed.gl.joinmc.link".\n If this does not work, @ or DM Skoshi to get help', inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="start-minecraft-server", description="Starts the Brackshots Minecraft Server", guild=GUILD)
@commands.has_any_role(MINECRAFT_ROLE_ID)
async def startMinecraftServer(interaction: discord.Interaction):
    with open("minecraftServer/status.json", "r") as f:
        running = json.loads(f.read())
        if not running:
            subprocess.Popen(["python3 serverMC.py"], cwd="minecraftServer", shell=True, stdin=subprocess.PIPE, stdout= subprocess.PIPE)
            await interaction.response.send_message("Starting Server")
        else:
            await interaction.response.send_message("Server already on")

client.run(TOKEN)

