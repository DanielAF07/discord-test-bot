import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

bot = commands.Bot(command_prefix='!')

async def get_last_id():
    channel = bot.get_channel(CHANNEL_ID)
    try:
        messages = await channel.history(limit=1).flatten()
        message = messages[0]
        print(f"message = {message}")
        if not message:
            return 1
        content = message.content
        if "UID: " not in content:
            return 1
        last_uid = content[content.find("UID: #") + 6: content.find("\n")]
        uid = int(last_uid) + 1
        return uid
    except:
        return 1

@bot.command(name='log', help='Log something.')
async def roll(ctx, title = None, description = None):
    if not title or not description:
        await ctx.send(f"""Command incomplete
        `!log "<title>" "<description>"`
        """)
        return 
    channel = bot.get_channel(CHANNEL_ID)
    uid = await get_last_id()
    await channel.send(f""">>> UID: #{uid}
    **{title}** by *{ctx.author.name}*
    {description}
    """)

@bot.command(name='dellog', help='Delete a log.')
async def roll(ctx, uid):
    if not uid or not uid.isnumeric():
        return await ctx.send("Error command. !dellog <uid>")
    channel = bot.get_channel(CHANNEL_ID)
    messages = await channel.history(limit=200).flatten()
    for message in messages:
        if uid in message.content:
            await message.delete()
            await ctx.send(f"Log #{uid} deleted")
            return
    return await ctx.send(f"Log #{uid} not found")

bot.run(TOKEN)