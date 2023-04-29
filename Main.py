import os
import openai
import discord
from discord.ext import commands

openai.api_key = os.environ.get('OPENAI_API_KEY')


async def get_gpt_response(prompt):
    messages = [
        {"role": "system", "content": "Talking to GrugBug, powered by BatGPT"},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        n=1,
        temperature=0.5,
    )

    return response.choices[0].message['content']

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="chat", help="Chat with the BatGPT AI")
async def chat(ctx, *, message):
    prompt = f"{ctx.author.name}: {message}"
    response = await get_gpt_response(prompt)
    await ctx.send(f"{bot.user.name}: {response}")

bot.run("MTEwMTY2NTkzMTU2ODEwMzQ0Ng.GC8C-6.PMfh7Jt5Ze3D5SIoclQI18nMn3tqj_4_cZH9pI")
