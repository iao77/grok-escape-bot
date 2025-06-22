import os
import json
import asyncio
import discord
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# --- Configuration initiale ---
load_dotenv()

# Récupération des variables (adapté à vos noms sur Railway)
TOKEN = os.getenv("JETON_BOT_DISCORD")  # Nom exact de votre variable
PORT = int(os.getenv("PORT", "8000"))    # Port obligatoire pour Railway
PYTHON_VERSION = os.getenv("VERSION_PYTHON", "3.10")

# Vérification critique du token
if not TOKEN:
    raise ValueError("❌ Token Discord manquant. Vérifiez que 'JETON_BOT_DISCORD' est bien défini dans les variables Railway.")

# --- Configuration Discord ---
intents = discord.Intents.default()
intents.message_content = True  # Nécessaire pour les commandes slash
intents.members = True         # Nécessaire pour les interactions serveur

client = commands.Bot(
    command_prefix="!", 
    intents=intents
)

# --- Gestion des données ---
try:
    with open('data.json', 'r') as f:
        user_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    user_data = {}

async def save_data():
    """Sauvegarde les données des utilisateurs"""
    with open('data.json', 'w') as f:
        json.dump(user_data, f)

# --- Gestion des erreurs ---
@client.event
async def on_error(event, *args, **kwargs):
    error = args[0] if args else 'Erreur inconnue'
    print(f"⚠️ Erreur dans {event}: {error}")
    await asyncio.sleep(5)
    await client.start(TOKEN)

@client.tree.error
async def on_slash_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(
        "🔧 Une erreur est survenue. Réessayez plus tard !",
        ephemeral=True
    )
    print(f"⚠️ Erreur de commande: {error}")

# --- Événements ---
@client.event
async def on_ready():
    print(f"✅ {client.user} est connecté (Python {PYTHON_VERSION})")
    try:
        synced = await client.tree.sync()
        print(f"🔗 {len(synced)} commandes synchronisées")
    except Exception as e:
        print(f"❌ Erreur de sync: {e}")

# --- Commandes ---
@client.tree.command(name="start", description="Démarre l'aventure Grok Escape")
async def start(interaction: discord.Interaction):
    """Initialise le jeu pour un nouvel utilisateur"""
    user_id = str(interaction.user.id)
    user_data[user_id] = user_data.get(user_id, {
        "fragments": 0,
        "recompenses": []
    })
    
    await interaction.response.send_message(
        "🎮 Bienvenue dans Grok Escape ! Utilisez /collect pour commencer.",
        ephemeral=True
    )
    await save_data()

@client.tree.command(name="collect", description="Collecte un fragment LOL")
async def collect(interaction: discord.Interaction):
    """Ajoute un fragment à l'utilisateur"""
    user_id = str(interaction.user.id)
    if user_id not in user_data:
        await start(interaction)
        return
    
    user_data[user_id]["fragments"] += 1
    total = user_data[user_id]["fragments"]
    
    await interaction.response.send_message(
        f"✨ Fragment LOL #{total} collecté ! (10 nécessaires pour s'échapper)",
        ephemeral=True
    )
    await save_data()

# --- Lancement ---
if __name__ == "__main__":
    try:
        print(f"🚀 Démarrage avec Python {PYTHON_VERSION}...")
        asyncio.run(client.start(TOKEN))
    except discord.LoginError:
        print("❌ Token Discord invalide. Vérifiez JETON_BOT_DISCORD.")
    except Exception as e:
        print(f"💥 Crash: {type(e).__name__}: {e}")
        with open('crash.log', 'a') as f:
            f.write(f"[{datetime.now()}] {str(e)}\n")
    finally:
        print("🛑 Bot arrêté")
