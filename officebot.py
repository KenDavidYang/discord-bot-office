import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
from discord.ui import Button, View
from random import randint, shuffle
from io import BytesIO
import requests, html, time, asyncio
# import praw # reddit tb fixed
import praw
import aiohttp

import atexit
print(discord.__version__)
print(discord.__file__)

# token and env initialization
load_dotenv()
TOKEN = os.getenv('TOKEN')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# reddit initialization
reddit = praw.Reddit (
    client_id = REDDIT_CLIENT_ID,
    client_secret = REDDIT_CLIENT_SECRET,
    user_agent = "default_bot 1.0 by default_user"
)

# test tb fixed
subreddit_name = "memes"
top_post = reddit.subreddit(subreddit_name).top(time_filter="day",limit=1)
for post in top_post:
    print(f"Title of the top post in r/{subreddit_name}: {post.title}")


# Create an instance of the bot with a command prefix, e.g., "!"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# default errors
error_messages = ("What", "🤨", "yep, that's an error", "pardon?", "wym", "idk what you meant",
                  "typo?", "wait, what?", "yo, stop playing with me. I don't like errors. Type properly like a civilized person",
                   "Add this to your list of errors:", "If this isn't a user error, it's not my fault either. Add 1 to the dev's headache counter",
                    "What was that? I coudln't quite hear you", "I don't understand", "もうわからん" 
                )

# mysql
import mysql.connector
from mysql.connector import Error

cnx = mysql.connector.connect(
    user = "default_user",
    password = MYSQL_PASSWORD,
    host = "localhost",
    database = "discord"
)

# channels
channels = {
    "general": 1391989365336707174,
    "cookies": 1391989487629893632,
    "trivia": 1391989523272957982,
    "memes": 1392342028985307289,
    "cats":1394132597587574965
}

# Event: when the bot is ready
@bot.event
async def on_ready():
    daily_reset()
    print(f'Logged in as {bot.user}')  # This confirms the bot is running.

    # Change the bot's status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for !trivia"))
    
    #reddit
    await post_top_reddit_to_discord()

    # daily trivia
    channel = bot.get_channel(channels["trivia"])
    cookie_channel = bot.get_channel(channels["cookies"])
    trivia_data = get_trivia()
    trivia_question = f"Trivia of The Day:\n\t{html.unescape(trivia_data['question'])}"
    correct_answer = html.unescape(trivia_data["correct_answer"])

    trivia_options = trivia_data["incorrect_answers"] + [trivia_data["correct_answer"]]
    trivia_options = [html.unescape(option) for option in trivia_options]
    shuffle(trivia_options)

    view = discord.ui.View()
    answered_users = set()

    def create_button(option):
        button = discord.ui.Button(label=option, style=discord.ButtonStyle.primary)

        async def callback(interaction):
            user = interaction.user

            if user.id in answered_users:
                await interaction.response.send_message(
                    "You have already answered this question.", ephemeral=True)
                return

            answered_users.add(user.id)

            if option == correct_answer:
                await interaction.response.send_message(f"{option} is Correct! ✅", ephemeral=True)
                await cookie_channel.send(f"{user.mention} won a cookie from Trivia! 🍪")
            else:
                await interaction.response.send_message(
                    f"{option} is Incorrect! ❌\nCorrect Answer: {correct_answer}", ephemeral=True
                )

        button.callback = callback
        return button

    for option in trivia_options:
        view.add_item(create_button(option))

    await channel.send(trivia_question, view=view)
    print("daily trivia sent!")

    await time_loop(duration_seconds=28800, 
                    interval_seconds=3600, 
                    function=lambda: get_cat("random"), 
                    channel_id=channels["cats"]
                    )

# Event: when the bot joins
@bot.event
async def on_guild_join(guild):
    channel = guild.system_channel  # Default system/welcome channel
    if channel:
        sticker = discord.Object(id=823976102976290866)
        await channel.send("Thanks for inviting me! Use !cookie to get a cookie...", stickers=[sticker]) # sticker limit is 3
 
#  loops
# @tasks.loop(hours=24)
# async def periodic_post():
#     await post_top_reddit_to_discord()
# then call
# periodic_post.start() 

# my functions
async def give_cookie(user):
    channel = bot.get_channel(channels["cookies"])
    try:
        if is_registered(user) == False:
            await channel.send(f"{user.mention}, you're not registered so no cookies for you ;(")
            await channel.send("Use !register to register (you'll get a free cookie)")
            return
        if not cnx.is_connected():
            cnx.reconnect()

        cursor = cnx.cursor()
        cursor.execute("UPDATE user_data SET cookies = cookies + 1 WHERE discord_id = %(discord_id)s", {'discord_id': user.id})

        if (randint(1, 11000) == 11): # arbitrary number
            cursor.execute("UPDATE user_data SET milk = milk + 1 WHERE discord_id = %(discord_id)s", {'discord_id': user.id})
            await channel.send(f"{user.mention} got milk! 🥛")

        cnx.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def close_db():
    if cnx.is_connected():
        cnx.close()
        print("Database connection closed.")

def get_trivia():
    """Returns a random trivia"""
    response = requests.get("https://opentdb.com/api.php?amount=1&category=9&difficulty=easy&type=multiple")
    if response.status_code == 200:
        data = response.json()
        one_result = data["results"][0]
        return one_result

def get_cat(type: str) -> tuple[BytesIO, str] | tuple[None, None]:
    """Fetches a cat image or gif and returns a (BytesIO, filename) tuple."""
    if type == "gif":
        url = "https://cataas.com/cat/gif"
        filename = "cat.gif"
    elif type == "img":
        url = "https://cataas.com/cat"
        filename = "cat.jpg"
    else:  # type == "random"
        if randint(0, 1):
            url = "https://cataas.com/cat/gif"
            filename = "cat.gif"
        else:
            url = "https://cataas.com/cat"
            filename = "cat.jpg"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BytesIO(response.content), filename
    except Exception as e:
        print(f"Error fetching cat: {e}")

    return None, None
    

def daily_reset():
    cursor = cnx.cursor()
    cursor.execute("UPDATE user_data SET daily_cookie = FALSE")
    cnx.commit()
    cursor.close()

def is_registered(user) -> bool:
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM users WHERE discord_id = %(discord_id)s", {"discord_id": user.id})
    result = cursor.fetchone()
    cursor.close()
    if result is None:
        return False
    else:
        return True

async def get_pokemon(pokemon: str) -> str:
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data["sprites"]["front_default"]
            else:
                return None

async def post_top_reddit_to_discord():
    """Function to fetch the top post from Reddit and send to Discord."""
    # Choose subreddit and get the top post of today
    subreddit_name = "memes"
    top_post = reddit.subreddit(subreddit_name).top(time_filter="day", limit=1)
    channel_meme = channels["memes"]

    for post in top_post:
        title = post.title
        url = post.url
        
        # Prepare the message content
        message_content = f"**Title**: {title}\n**Link**: {post.url}"
        
        # Check for media type (image, gif, or video)
        if url.endswith(('jpg', 'jpeg', 'png', 'gif', 'gifv')):
            # If it's an image or gif, send as an embed
            embed = discord.Embed(title=title, url=url)
            embed.set_image(url=url)
            await bot.get_channel(channel_meme).send(embed=embed)
        elif "v.redd.it" in url:
            # If it's a video, send the video URL
            embed = discord.Embed(title=title, url=url)
            embed.add_field(name="Video", value="Here's a Reddit-hosted video", inline=False)
            await bot.get_channel(channel_meme).send(embed=embed)
        else:
            # If no media, send just the text
            await bot.get_channel(channel_meme).send(message_content)

async def time_loop(duration_seconds, interval_seconds, function, channel_id):
    channel = bot.get_channel(channel_id)
    start_time = time.time()
    while (time.time() - start_time) < duration_seconds:
        result = function()
        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], BytesIO):
            file_data, file_name = result
            if file_data:
                await channel.send(file=discord.File(file_data, filename=file_name))
        else:
            if result:
                await channel.send(result)
        await asyncio.sleep(interval_seconds)


# Command: !hello (Simple command)
@bot.command()
async def hello(ctx):
    print("Hello command triggered!")
    await ctx.send("Hello! I'm your bot.")  # Sends a message in the channel

@bot.command()
async def cookie(ctx):
    cookie_channel = bot.get_channel(channels["cookies"])
    user = ctx.author
    cursor = cnx.cursor()
    cursor.execute("SELECT daily_cookie FROM user_data WHERE discord_id = %(user_id)s", {"user_id": user.id})
    result = cursor.fetchone()

    if is_registered(user) is None:
        await ctx.send("You are not registered yet. Please register first.")
    else:
        daily_cookie = result[0]  # True or False (stored as 1 or 0)
        if not daily_cookie:  # If daily cookie has not been claimed yet
            await cookie_channel.send(f"{user.mention} claimed a daily cookie 🍪")
            await give_cookie(user)

            cursor.execute("UPDATE user_data SET daily_cookie = TRUE WHERE discord_id = %(user_id)s", {"user_id": user.id})
            cnx.commit()
        else:
            await ctx.send("Don't be greedy, you already claimed your daily cookie today")

    cursor.close()


@bot.command()
async def cookie_count(ctx):
    cursor = cnx.cursor()
    user = ctx.author
    cursor.execute("SELECT cookies FROM user_data WHERE discord_id = %(discord_id)s", {"discord_id": user.id})

    result = cursor.fetchone()
    await ctx.send(f"You have {result[0]} cookies! 🍪")
    cursor.close()

@bot.command()
async def d20(ctx):
    await ctx.send(randint(1, 20))

@bot.command()
async def cat(ctx):
    random_number = randint(1, 11)
    if random_number == 11:
        await ctx.send(file=discord.File("pop_cat.png"))
    elif random_number >= 5:
        await ctx.send(get_cat("img")[0])  
    else :
        await ctx.send(get_cat("gif")[0])

@bot.command()
async def register(ctx):
    user = ctx.author
    username = str(user)
    discord_id = user.id

    add_user = ("INSERT INTO users (discord_id, username) VALUES (%(discord_id)s, %(username)s)")
    add_user_data = ("INSERT INTO user_data (discord_id) VALUES (%(discord_id)s)") 
    user_data = {
        "discord_id": discord_id, 
        "username": username
    }
    
    try:
        cursor = cnx.cursor()
        cursor.execute(add_user, user_data)
        cursor.execute(add_user_data, {"discord_id": discord_id} )
        cnx.commit()

        await ctx.send(f"{user.mention} has been registered! You get an appreciation cookie 🍪")
        await give_cookie(user)
    except Error as e:
        cnx.rollback()
        if e.errno == 1062:  # Duplicate entry error code
            print(f"Error: User with discord_id: {discord_id} already exists.")
            await ctx.send("User has already been registered.")
        else:
            print(f"Unexpected error: {e}")
    finally:
        if cursor:
            cursor.close()

@bot.command()
async def pokemon(ctx, pokemon: str):
    pokemon_sprite = await get_pokemon(pokemon)

    if pokemon_sprite:
        embed = discord.Embed()
        embed.set_image(url=pokemon_sprite)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Who's that pokemon? (cause that ain't a pokemon lmao)")

# Run the bot with your token
atexit.register(close_db)
bot.run(TOKEN)  # Replace this with your actual bot token
