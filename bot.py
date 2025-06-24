import os, json, discord
from discord.ext import commands

# Chargement des données
DATA_FILE = "data.json"
def load_data():
    if not os.path.exists(DATA_FILE): return {}
    with open(DATA_FILE, "r") as f: return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=2)

# Configuration du bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est connecté")
    guild_id = os.getenv("ID_GUILDE")
    if guild_id:
        guild = discord.Object(id=int(guild_id))
        try:
            synced = await tree.sync(guild=guild)
            print(f"🔗 {len(synced)} slash commands synchronisées pour la guilde {guild_id}")
        except Exception as e:
            print(f"❌ Erreur de sync : {e}")
    else:
        print("❌ ID_GUILDE non défini dans les variables Railway")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🚀 Pong ! Latence : {round(bot.latency * 1000)}ms")

@tree.command(name="start", description="Commence à jouer à Grok Escape")
async def start(interaction: discord.Interaction):
    user = str(interaction.user.id)
    data = load_data()
    if user not in data:
        data[user] = {"fragments": 1, "rewards": []}
        msg = "Bienvenue ! Tu as reçu ton 1er fragment LOL 🎉"
    else:
        msg = "Tu as déjà commencé, continue à jouer !"
    save_data(data)
    await interaction.response.send_message(msg, ephemeral=True)

@tree.command(name="score", description="Affiche tes fragments LOL")
async def score(interaction: discord.Interaction):
    user = str(interaction.user.id)
    fragments = load_data().get(user, {}).get("fragments", 0)
    await interaction.response.send_message(f"💎 Tu as {fragments} fragments LOL.", ephemeral=True)

@tree.command(name="rewards", description="Liste tes récompenses")
async def rewards(interaction: discord.Interaction):
    user = str(interaction.user.id)
    rewards = load_data().get(user, {}).get("rewards", [])
    txt = "\n".join(rewards) if rewards else "Aucune récompense encore !"
    await interaction.response.send_message(f"🎁 Récompenses :\n{txt}", ephemeral=True)

@tree.command(name="escape", description="S'échapper avec 10 fragments")
async def escape(interaction: discord.Interaction):
    user = str(interaction.user.id)
    data = load_data()
    fragments = data.get(user, {}).get("fragments", 0)
    if fragments >= 10:
        data[user]["fragments"] = 0
        data[user]["rewards"].append("Libération 🏃")
        msg = "🚪 Tu t'es échappé !"
    else:
        msg = f"❌ Il te faut 10 fragments. Tu en as {fragments}."
    save_data(data)
    await interaction.response.send_message(msg, ephemeral=True)

bot.run(os.getenv("JETON_BOT_DISCORD"))
