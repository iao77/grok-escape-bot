import os
import discord
from discord.ext import commands

# Intents Discord complets
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Slash commands (Arbre)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est connecté")
    try:
        synced = await tree.sync()
        print(f"🔗 {len(synced)} slash commands synchronisées")
    except Exception as e:
        print(f"❌ Erreur de sync : {e}")

# Commande classique (préfixe "!")
@bot.command()
async def ping(ctx):
    await ctx.send(f"🚀 Pong ! Latence : {round(bot.latency * 1000)}ms")

# Slash command de test
@tree.command(name="start", description="Lance le jeu Grok Escape")
async def start_command(interaction: discord.Interaction):
    await interaction.response.send_message("Bienvenue dans Grok Escape ! 🔓", ephemeral=True)

bot.run(os.getenv("JETON_BOT_DISCORD"))
