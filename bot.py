import os
import json
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Configuration initiale
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents requis
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

# Stockage des données
try:
    with open('data.json', 'r') as f:
        user_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    user_data = {}

# Sauvegarde automatique
async def save_data():
    with open('data.json', 'w') as f:
        json.dump(user_data, f)

# Gestion des erreurs
@client.event
async def on_error(event, *args, **kwargs):
    error = args[0] if args else 'Unknown error'
    print(f"⚠️ Error in {event}: {error}")
    await asyncio.sleep(5)
    await client.start(TOKEN)

@client.tree.error
async def on_slash_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(
        "🔧 Le bot rencontre un problème... Réessayez plus tard !",
        ephemeral=True
    )
    print(f"⚠️ Slash Command Error: {error}")

# Événements
@client.event
async def on_ready():
    print(f"✅ {client.user} est opérationnel")
    try:
        synced = await client.tree.sync()
        print(f"🔗 {len(synced)} commandes synchronisées")
    except Exception as e:
        print(f"❌ Sync error: {e}")

# Commandes
@client.tree.command(name="start", description="Démarre l'aventure")
async def start(interaction: discord.Interaction):
    """Commande de démarrage"""
    user_id = str(interaction.user.id)
    user_data[user_id] = user_data.get(user_id, {"fragments": 0, "rewards": []})
    
    await interaction.response.send_message(
        "🎮 Aventure lancée ! Utilisez /collect pour gagner des fragments.",
        ephemeral=True
    )
    await save_data()

@client.tree.command(name="collect", description="Collecte des fragments")
async def collect(interaction: discord.Interaction):
    """Collecte des fragments LOL"""
    user_id = str(interaction.user.id)
    if user_id not in user_data:
        await start(interaction)
        return
    
    user_data[user_id]["fragments"] += 1
    fragments = user_data[user_id]["fragments"]
    
    await interaction.response.send_message(
        f"✨ Fragment LOL #{fragments} collecté ! (10 nécessaires pour s'échapper)",
        ephemeral=True
    )
    await save_data()

@client.tree.command(name="escape", description="Tente de s'échapper")
async def escape(interaction: discord.Interaction):
    """Tentative d'évasion"""
    user_id = str(interaction.user.id)
    if user_id not in user_data:
        await start(interaction)
        return
    
    if user_data[user_id]["fragments"] >= 10:
        await interaction.response.send_message(
            "🏆 FÉLICITATIONS ! Tu t'es échappé du Sérieux Absolu !",
            ephemeral=False
        )
    else:
        await interaction.response.send_message(
            f"🔐 Il te faut {10 - user_data[user_id]['fragments']} fragments supplémentaires !",
            ephemeral=True
        )

# Lancement
if __name__ == "__main__":
    try:
        print("🚀 Démarrage du bot...")
        asyncio.run(client.start(TOKEN))
    except Exception as e:
        print(f"💥 Crash: {e}")
        with open('crash.log', 'a') as f:
            f.write(f"Crash at {datetime.now()}: {str(e)}\n")
