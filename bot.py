import os
import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True  # Nécessaire pour les commandes slash
intents.members = True         # Nécessaire pour les interactions serveur
client = commands.Bot(command_prefix="!", intents=intents)

# ========= Gestion des erreurs =========
@client.event
async def on_error(event, *args, **kwargs):
    print(f"[ERREUR] Sur l'événement {event}: {args[0] if args else 'Erreur inconnue'}")

@client.tree.error
async def on_slash_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(
        "⚠️ Une erreur est survenue. Réessayez plus tard.",
        ephemeral=True
    )
    print(f"[ERREUR SLASH] {error}")

# ========= Événements =========
@client.event
async def on_ready():
    print(f"{client.user} est connecté !")
    try:
        synced = await client.tree.sync()
        print(f"Commandes slash synchronisées ({len(synced)}): {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"Erreur de sync: {e}")

# ========= Commandes =========
@client.tree.command(name="start", description="Lance le jeu d'évasion")
async def start(interaction: discord.Interaction):
    """Commande de démarrage du jeu"""
    await interaction.response.send_message(
        "🔐 Aventure lancée ! Prépare-toi à t'échapper...",
        ephemeral=True
    )

# ========= Lancement =========
if __name__ == "__main__":
    try:
        print("Démarrage du bot...")
        asyncio.run(client.start(TOKEN))
    except discord.LoginError:
        print("ERREUR: Token Discord invalide")
    except Exception as e:
        print(f"ERREUR FATALE: {e}")
    finally:
        print("Bot arrêté")
