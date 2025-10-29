import discord
from discord.ext import commands
from config import TOKEN
from config import GUILDS

print(discord.__version__)
print(discord.__file__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


# tb implemented
async def setup_hook():
    print("Loading cogs...")
    try:
        await bot.load_extension('cogs.cat')
        await bot.load_extension('cogs.cookie')
        await bot.load_extension('cogs.events') 
        await bot.load_extension('cogs.fabula') 
        await bot.load_extension('cogs.lama') 
        await bot.load_extension('cogs.limbo')
        await bot.load_extension('cogs.pokemon')
        await bot.load_extension('cogs.reddit')
        await bot.load_extension('cogs.trivia')
        
        # uncomment for specific guild or testing
        # await bot.tree.sync(guild=discord.Object(id=GUILDS["default_marketing_server"]))

        # uncomment for all guilds
        await bot.tree.sync()
        print("Cogs loaded successfully.")
        
    except Exception as e:
        print(f"Failed to load cog: {e}")
        
bot.setup_hook = setup_hook

# Event: when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    # Bot Status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for !trivia"))

bot.run(TOKEN) 

# import atexit
# atexit.register(close_db)

# async def time_loop(duration_seconds, interval_seconds, function, channel_id):
#     channel = bot.get_channel(channel_id)
#     start_time = time.time()
#     while (time.time() - start_time) < duration_seconds:
#         result = function()
#         if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], BytesIO):
#             file_data, file_name = result
#             if file_data:
#                 await channel.send(file=discord.File(file_data, filename=file_name))
#         else:
#             if result:
#                 await channel.send(result)
#         await asyncio.sleep(interval_seconds)

#  loops
# @tasks.loop(hours=24)
# async def periodic_post():
#     await post_top_reddit_to_discord()
# then call
# periodic_post.start() 

# @bot.hybrid_group(fallback="get")
# async def tag(ctx, name):
#     await ctx.send(f"Showing tag: {name}")

# @tag.command()
# async def create(ctx, name):
#     await ctx.send(f"Created tag: {name}")