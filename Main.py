import os
import openai
import discord
from discord.ext import commands
from discord import Intents

# Get OPEN_API_KEY from window environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')


"""
Function that receives a prompt from user, feeds the prompt into a GPT model, and returns the GPT response
:param prompt: Only argument, holds the prompt passed from user
:return: The response from the GPT model
"""
async def get_gpt_response(prompt):

    # List of messages, first element is system message, second element is user message
    messages = [
        {"role": "system", "content": "Talking to GrugBug, powered by BatGPT"},
        {"role": "user", "content": prompt}
    ]

    # Call OpenAI API with provided prompt 'prompt', using 3.5 model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        n=1,
        temperature=0.5,
    )

    # return generated response from GPT model
    return response.choices[0].message['content']


# get default intents, and enables messages, guilds, and message content intent
intents = Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Create Discord bot instance, with command prefix '!' and defined intents
bot = commands.Bot(command_prefix="!", intents=intents)


'''
Async function that runs when bot is ready and connected to discord, prints message to console
'''
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


"""
Async function that runs when a message is received (with command_prefix), processes the message sent
:param message: represents the message that the discord user sent, for the bot to process
"""
@bot.event
async def on_message(message):
    # If message is from bot itself, simply returns (dont need to process)
    if message.author == bot.user:
        return
    # Otherwise, process commands in received message
    await bot.process_commands(message)


"""
Async command function that interacts with GPT AI
"""
@bot.command(name="chat", help="Chat with the BatGPT AI")
async def chat(ctx, *, message):
    # Create prompt using message content and author's name
    prompt = f"{ctx.author.name}: {message}"
    # calls GPT response using other func, assigns return value to 'response'
    response = await get_gpt_response(prompt)
    # Send the response as a message in the chat
    await ctx.send(f"{bot.user.name}: {response}")


"""
Main function, runs on program start
"""
def main():
    # Get Discord bot key from Windows environment variable
    discord_bot_key = os.environ.get('DISCORD_BOT_KEY')
    # Run bot, using Discord bot key
    bot.run(discord_bot_key)


# Run main func
if __name__ == "__main__": main()


