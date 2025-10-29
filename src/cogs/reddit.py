import discord
from discord.ext import commands
from api import reddit

# test tb fixed
async def get_top_post(subreddit_name):
    top_post = reddit.subreddit(subreddit_name).top(time_filter="day",limit=1)
    for post in top_post:
        print(f"Title of the top post in r/{subreddit_name}: {post.title}")

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._posted_on_start = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self._posted_on_start:
            await self.post_top_reddit_to_discord()
            self._posted_on_start = True

    async def post_top_reddit_to_discord(self):
        """Function to fetch the top post from Reddit and send to Discord."""
        subreddit_name = "memes"
        # top_post = reddit.subreddit(subreddit_name).top(time_filter="day", limit=1)
        channel_meme = 1389905084015706135

        top_post = (await reddit.subreddit(subreddit_name)).top(time_filter="day", limit=1)

        async for post in top_post:
            title = post.title
            url = post.url
            
            message_content = f"**Title**: {title}\n**Link**: {post.url}"
            
            if url.endswith(('jpg', 'jpeg', 'png', 'gif', 'gifv')):
                # If it's an image or gif, send as an embed
                embed = discord.Embed(title=title, url=url)
                embed.set_image(url=url)
                await self.bot.get_channel(channel_meme).send(embed=embed)
            elif "v.redd.it" in url:
                # If it's a video, send the video URL
                embed = discord.Embed(title=title, url=url)
                embed.add_field(name="Video", value="Here's a Reddit-hosted video", inline=False)
                await self.bot.get_channel(channel_meme).send(embed=embed)
            else:
                # If no media, send just the text
                await self.bot.get_channel(channel_meme).send(message_content)

async def setup(bot):
    await bot.add_cog(Reddit(bot))
