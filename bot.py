import os
import discord
from discord.ext import commands

# Vérification stricte du token
TOKEN = os.getenv("JETON_BOT_DISCORD")
if not TOKEN:
    raise ValueError("""
    ERREUR CRITIQUE :
    Le token Discord est introuvable.
    Vérifiez que :
    1. La variable 'JETON_BOT_DISCORD' existe bien dans Railway
    2. Le nom est exactement le même (sans espaces)
    3. Le token est valide (non expiré)
    """)

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user.name} connecté avec succès !")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong !")

bot.run(TOKEN)
