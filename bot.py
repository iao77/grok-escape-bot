import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} est en ligne !")
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)} commande(s) slash synchronisée(s).")
    except Exception as e:
        print(f"Erreur de sync : {e}")

@client.tree.command(name="start", description="Lance une partie d'évasion !")
async def start(interaction: discord.Interaction):
    await interaction.response.send_message("🔐 Tu as lancé la partie. Prépare-toi à t’échapper !")

client.run(TOKEN)