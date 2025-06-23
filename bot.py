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
    guild_id = os.getenv("GUILD_ID")  # Récupère l'ID de la guilde depuis les variables d'environnement
    if guild_id:
        guild = discord.Object(id=int(guild_id))  # Convertit l'ID en objet Discord
        try:
            synced = await tree.sync(guild=guild)  # Synchronisation spécifique à la guilde
            print(f"🔗 {len(synced)} slash commands synchronisées pour la guilde {guild_id}")
        except Exception as e:
            print(f"❌ Erreur de sync : {e}")
    else:
        print("❌ GUILD_ID non défini dans les variables d'environnement")

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
