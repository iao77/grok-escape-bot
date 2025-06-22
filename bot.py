import os

TOKEN = os.getenv("JETON_BOT_DISCORD")
print("Token récupéré :", "****" + TOKEN[-4:] if TOKEN else "AUCUN TOKEN TROUVÉ")

if not TOKEN:
    raise RuntimeError("""
    ERREUR : Variable 'JETON_BOT_DISCORD' manquante.
    Vérifiez que :
    1. Le nom est EXACTEMENT 'JETON_BOT_DISCORD' (copiez-collez ce nom)
    2. La variable est bien sauvegardée (onglet Variables → bouton Save)
    """)

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    await bot.change_presence(activity=discord.Game(name="/start"))

bot.run(TOKEN)
