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
    # If message is from bot itself, simply returns (don't need to process)
    if message.author == bot.user:
        return

    # Otherwise, process commands in received message
    # Check if bot is mentioned in the message
    if bot.user in message.mentions:
        # Process if the message contains an image attachment by calling other func
        contains_image = await process_image(message)
        if contains_image:
            print("image done, do OCR here")
            return
        else:
            # Remove bot mention from message content, strip leading/trailing whitespace
            cleaned_message = message.content.replace(f'<@!{bot.user.id}>', '').strip()
            # Call chat function, with context and cleaned_message
            ctx = await bot.get_context(message)
            await chat(ctx, message=cleaned_message)
    else:
        # Otherwise, process commands in received message
        await bot.process_commands(message)


"""
Function that processes if a message contains an image attachment
:param message: represents the message that is to be processed, to see if it contains an image attachment
:return: A boolean that is True if image has been processed, for False otherwise
"""
async def process_image(message) -> bool:
    # Check if message has attachment
    if message.attachments:
        for attachment in message.attachments:
            # Check if attachment is img (jpg / png)
            if attachment.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Save image locally
                save_directory = 'Images'
                # exist_ok=True means that function won't raise error if directory already exists
                os.makedirs(save_directory, exist_ok=True)
                image_path = os.path.join(save_directory, attachment.filename)
                await attachment.save(image_path)
                await message.channel.send(f"Image saved as {attachment.filename}")
                return True
    return False


"""
Async command function that interacts with GPT AI
:param ctx: abbreviation for context, an instance of 'commands.Context', provides context around the function call,
            such as ctx.author (user who invoked command), ctx.channel (channel where command was invoked), etc.
:param *: specifies that arguments after the '*' (i.e., 'message') are passed as keyword arguments, not positional
:param message: captures remaining content of command as a string
"""
# Decorator that registers 'chat' as aa command in discord bot, and 'help' parameter give users explanation of the bot
@bot.command(name="GrugBug", help="Chat with the BatGPT AI")
async def chat(ctx, *, message):
    # Create prompt using message content and author's name
    prompt = f"{ctx.author.name}: {message}"
    # calls GPT response using other func, assigns return value to 'response'
    response = await get_gpt_response(prompt)
    # Send the response as a message in the chat
    await ctx.send(f"{ctx.author.mention}, {response}")


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


