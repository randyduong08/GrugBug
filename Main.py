import os
import openai
import discord
from discord.ext import commands
from discord import Intents

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

intents = Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


@bot.command(name="chat", help="Chat with the BatGPT AI")
async def chat(ctx, *, message):
    prompt = f"{ctx.author.name}: {message}"
    response = await get_gpt_response(prompt)
    await ctx.send(f"{bot.user.name}: {response}")


def main():
    discord_bot_key = os.environ.get('DISCORD_BOT_KEY')
    bot.run(discord_bot_key)


if __name__ == "__main__": main()


