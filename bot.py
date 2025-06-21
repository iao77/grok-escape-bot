import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Nécessaire pour les commandes slash
client = commands.Bot(command_prefix="!", intents=intents)

# --- Gestion des erreurs ---
@client.event
async def on_error(event, *args, **kwargs):
    print(f"[ERREUR] Événement {event} : {args[0] if args else 'Inconnue'}")

@client.tree.error
async def on_slash_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(
        f"⚠️ Une erreur est survenue : {str(error)}",
        ephemeral=True
    )
    print(f"[SLASH_ERR] {error}")

# --- Événements ---
@client.event
async def on_ready():
    print(f"{client.user} est en ligne !")
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)} commande(s) slash synchronisée(s).")
    except Exception as e:
        print(f"Erreur de sync : {e}")

# --- Commandes ---
@client.tree.command(name="start", description="Lance une partie d'évasion !")
async def start(interaction: discord.Interaction):
    await interaction.response.send_message("🔐 Tu as lancé la partie. Prépare-toi à t’échapper !")

# --- Lancement ---
if __name__ == "__main__":
    try:
        client.run(TOKEN)
    except Exception as e:
        print(f"[CRASH] Erreur fatale : {e}")
        raise
