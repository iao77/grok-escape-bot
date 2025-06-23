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
    guild = discord.Object(id=1383331599201992704)  # Synchronisation par guilde (ton serveur)
    try:
        synced = await tree.sync(guild=guild)
        print(f"🔗 {len(synced)} slash commands synchronisées pour la guilde")
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

# Nouvelle commande slash : /score
@tree.command(name="score", description="Affiche ton score")
async def score_command(interaction: discord.Interaction):
    await interaction.response.send_message("Ton score : 0 points (à implémenter)", ephemeral=True)

# Nouvelle commande slash : /rewards
@tree.command(name="rewards", description="Affiche tes récompenses")
async def rewards_command(interaction: discord.Interaction):
    await interaction.response.send_message("Aucune récompense pour l'instant (à implémenter)", ephemeral=True)

# Nouvelle commande slash : /escape
@tree.command(name="escape", description="Tente de t'échapper")
async def escape_command(interaction: discord.Interaction):
    await interaction.response.send_message("Évasion en cours... (à implémenter)", ephemeral=True)

bot.run(os.getenv("JETON_BOT_DISCORD"))
