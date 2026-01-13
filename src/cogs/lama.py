import ollama
from ollama import chat, web_fetch, web_search
from discord.ext import commands
import textwrap
from config import OLLAMA_API_KEY
import os

os.environ["OLLAMA_API_KEY"] = OLLAMA_API_KEY

class Lama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = ollama.Client()
        self.model = "llama3.2"

    @commands.command()
    async def hey(self, ctx, *, prompt):
        await ctx.typing()
        response = self.client.generate(model=self.model, prompt=prompt + "keep it within 2000 characters, shorter the better, but take as much characters as you need")

        if (len(response.response) > 2000):
            await ctx.send(response.response[:1997] + "...")
        else:
            await ctx.send(response.response)

    # @commands.command()
    # async def search(self, ctx, *, prompt):
    #     await ctx.typing()
        # response = ollama.web_search(prompt + "keep it within 2000 characters, shorter the better, but take as much characters as you need")

        # print(f"response: {type(response)}")
        # print(f"response: {dir(response)}")
        # print(f"response: {response.results}")

        # message_chunks = textwrap.wrap(response, width=2000, break_long_words=True, replace_whitespace=False)

        # for i, chunk in enumerate(message_chunks):
        #     header = f"**Search Result (Part {i + 1}/{len(message_chunks)})**\n"

        #     if len(header) + len(chunk) <= 2000:
        #         await ctx.send(header + chunk)
        #     else:
        #         await ctx.send(chunk)
        # context = response.results
        # if(len(content) > 2000):
        #     await ctx.send(content[:1997] + "...")
        # else:
        #     await ctx.send(content)


        # available_tools = {"web_search": web_search, "web_fetch": web_fetch}
        # messages = [{"role": "user", "content": prompt}]

        # while True:
        #     response = chat(
        #         model=self.model,
        #         messages=messages,
        #         tools=[web_search, web_fetch],
        #         think=True
        #     )

        #     if response.message.thinking:
        #         print("Thinking: ", response.message.thinking)
        #     if response.message.content:
        #         print("Content: ", response.message.content)
        #     messages.append(response.message)

        #     if response.message.tool_calls:
        #         print("Tool Calls: ", response.message.tool_calls)

        #         for tool_call in response.message.tool_calls:
        #             function_to_call = available_tools.get(tool_call.function.name)

        #             if function_to_call:
        #                 args = tool_call.function.arguments
        #                 result = function_to_call(**args)

        #                 print("Result: ", str(result)[:200]+"...")
        #                 # Result is truncated for limited message length
        #                 messages.append({'role': 'tool', 'content': str(result)[:2000 * 4], 'tool_name': tool_call.function.name})
        #             else:
        #                 messages.append({'role': 'tool', 'content': f'Tool {tool_call.function.name} not found', 'tool_name': tool_call.function.name})
                
        #     else:
        #         break

        

async def setup(bot):
    await bot.add_cog(Lama(bot))