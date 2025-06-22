import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import random
import json
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID") # Récupérer l'ID de la guilde depuis les variables d'environnement

# Utilisation de discord.Intents.all() pour le debug
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

# Probabilités du jeu
PROBA_FRAGMENT = 0.7
PROBA_PIÈGE = 0.2
PROBA_RARE_FRAGMENT = 0.1

# Messages humoristiques Grok-style
MSG_FRAGMENT = "Fragment LOL capturé ! Le multivers rit à gorge déployée ! 🌀"
MSG_PIÈGE = "Aïe ! Tableau Excel sérieux ! Tu perds un tour... Respire, on rigolera plus tard. 🕳️"
MSG_RARE_FRAGMENT = "Wow ! Fragment rare détecté ! Une aura de LOL t'entoure ! ✨"

DATA_FILE = "data.json"

# --- FONCTIONS UTILITAIRES POUR data.json ---

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_player_data(user_id):
    data = load_data()
    return data.get(str(user_id), {"fragments": 0, "skip_turn": 0, "rewards": []})

def update_player_data(user_id, fragments=None, skip_turn=None, rewards=None):
    data = load_data()
    user_id_str = str(user_id)
    if user_id_str not in data:
        data[user_id_str] = {"fragments": 0, "skip_turn": 0, "rewards": []}

    if fragments is not None:
        data[user_id_str]["fragments"] = fragments
    if skip_turn is not None:
        data[user_id_str]["skip_turn"] = skip_turn
    if rewards is not None:
        data[user_id_str]["rewards"] = rewards
    save_data(data)

# --- COMMANDES CLASSIQUES ---

@client.command(name="ping")
async def ping_command(ctx):
    latency = round(client.latency * 1000)
    await ctx.send(f"Pong ! {latency}ms")

# --- COMMANDES SLASH ---

@client.tree.command(name="start", description="Lance une partie d'évasion !")
async def start_slash(interaction: discord.Interaction):
    user_id = interaction.user.id
    player_data = get_player_data(user_id)
    update_player_data(user_id, fragments=player_data["fragments"], skip_turn=player_data["skip_turn"], rewards=player_data["rewards"])

    embed = discord.Embed(
        title="Bienvenue dans Grok Escape !",
        description=f"Lance ta quête avec `/collect` et échappe-toi du Sérieux Absolu, {interaction.user.mention} ! 🌀",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url="https://i.imgur.com/your_grok_image.png") # Placeholder for a Grok image
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="collect", description="Tente de récupérer un fragment LOL !")
async def collect_slash(interaction: discord.Interaction):
    user_id = interaction.user.id
    player_data = get_player_data(user_id)
    fragments = player_data["fragments"]
    skip_turn = player_data["skip_turn"]

    if skip_turn > 0:
        update_player_data(user_id, skip_turn=skip_turn - 1)
        embed = discord.Embed(
            title="Piège du Sérieux !",
            description=f"{interaction.user.mention}, tu es coincé dans un piège sérieux, tu perds ce tour ! 🕳️",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return

    roll = random.random()
    if roll <= PROBA_FRAGMENT:
        fragments += 1
        update_player_data(user_id, fragments=fragments)
        embed = discord.Embed(
            title="Fragment LOL capturé !",
            description=f"{interaction.user.mention} {MSG_FRAGMENT} (Total fragments: {fragments})",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    elif roll <= PROBA_FRAGMENT + PROBA_PIÈGE:
        update_player_data(user_id, skip_turn=1)
        embed = discord.Embed(
            title="Piège du Sérieux !",
            description=f"{interaction.user.mention} {MSG_PIÈGE}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        fragments += 1
        update_player_data(user_id, fragments=fragments)
        embed = discord.Embed(
            title="Fragment Rare Détecté !",
            description=f"{interaction.user.mention} {MSG_RARE_FRAGMENT} (Total fragments: {fragments})",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)

@client.tree.command(name="score", description="Affiche le classement des éclaireurs du rire.")
async def score_slash(interaction: discord.Interaction):
    data = load_data()
    # Convert user_ids to mentions for display
    leaderboard_data = []
    for user_id_str, player_data in data.items():
        try:
            user = await client.fetch_user(int(user_id_str))
            leaderboard_data.append((user.mention, player_data["fragments"]))
        except discord.NotFound:
            leaderboard_data.append((f"Utilisateur Inconnu ({user_id_str})", player_data["fragments"]))

    leaderboard_data.sort(key=lambda x: x[1], reverse=True)
    top_5 = leaderboard_data[:5]

    if not top_5:
        description = "Aucun joueur enregistré pour le moment."
    else:
        description = "\n".join([f"{mention} : {frags} fragments LOL" for mention, frags in top_5])

    embed = discord.Embed(
        title="🏆 Top 5 des éclaireurs du rire :",
        description=description,
        color=discord.Color.purple()
    )
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="escape", description="Tente de t'échapper du Labyrinthe Cosmique !")
async def escape_slash(interaction: discord.Interaction):
    user_id = interaction.user.id
    player_data = get_player_data(user_id)
    fragments = player_data["fragments"]
    rewards = player_data["rewards"]

    if fragments >= 10:
        update_player_data(user_id, fragments=0) # Reset fragments after escape
        reward_name = "Badge Maître du LOL"
        if reward_name not in rewards:
            rewards.append(reward_name)
            update_player_data(user_id, rewards=rewards)

        embed = discord.Embed(
            title="🎉 Évasion Réussie ! 🎉",
            description=f"{interaction.user.mention} a brisé la malédiction du Sérieux Absolu ! Le multivers rit grâce à toi ! Tu as gagné le {reward_name} ! 🌀",
            color=discord.Color.orange()
        )
        embed.set_footer(text="Manus génère un mème IA personnalisé pour célébrer ta victoire !")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Quête en Cours...",
            description=f"{interaction.user.mention}, il te faut 10 fragments LOL pour t'échapper ! Actuellement : {fragments}.",
            color=discord.Color.greyple()
        )
        await interaction.response.send_message(embed=embed)

@client.tree.command(name="rewards", description="Affiche tes récompenses gagnées.")
async def rewards_slash(interaction: discord.Interaction):
    user_id = interaction.user.id
    player_data = get_player_data(user_id)
    rewards = player_data["rewards"]

    if not rewards:
        description = f"{interaction.user.mention}, tu n'as pas encore de récompenses. Continue à jouer pour en gagner !"
    else:
        description = "\n".join([f"- {reward}" for reward in rewards])

    embed = discord.Embed(
        title="🎁 Tes récompenses :",
        description=description,
        color=discord.Color.teal()
    )
    await interaction.response.send_message(embed=embed)

# --- EVENT ON READY ---

@client.event
async def on_ready():
    print(f"{client.user} est en ligne !")
    try:
        # Synchronisation des commandes slash avec la guilde spécifique
        guild = discord.Object(id=int(GUILD_ID))
        client.tree.copy_global_to(guild=guild)
        synced = await client.tree.sync(guild=guild)
        print(f"{len(synced)} commande(s) slash synchronisée(s) avec la guilde {GUILD_ID}.")
    except Exception as e:
        print(f"Erreur de sync : {e}")

# --- LANCEMENT BOT ---

client.run(TOKEN)
    
