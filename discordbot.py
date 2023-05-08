from discord.ext import commands
from discord import Intents
from image_processing import capture_image, ocr_image
from gpt import get_gpt_response

class DiscordBot:

    def __init__(self):
        # get default intents, and enables messages, guilds, and message content intent
        intents = Intents.default()
        intents.messages = True
        intents.guilds = True
        intents.message_content = True

        # Create Discord bot instance, with command prefix '!' and defined intents
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.register_events()
        self.register_commands()

    def register_events(self):
        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)

    def register_commands(self):
        # Decorator that registers 'chat' as aa command in discord bot, and 'help' parameter
        # give users explanation of the bot
        self.bot.command(name="GrugBug", help="Chat with the BatGPT AI")(self.chat)

    '''
    Async function that runs when bot is ready and connected to discord, prints message to console
    '''
    async def on_ready(self):
        print(f"{self.bot.user.name} has connected to Discord!")

    """
    Async function that runs when a message is received (with command_prefix), processes the message sent
    :param message: represents the message that the discord user sent, for the bot to process
    """
    async def on_message(self, message):
        # If message is from bot itself, simply returns (don't need to process)
        if message.author == self.bot.user:
            return

        # Otherwise, process commands in received message
        # Check if bot is mentioned in the message
        if self.bot.user in message.mentions:
            # Process if the message contains an image attachment by calling other func
            contains_image, img = await capture_image(message)
            if contains_image:
                print("image done, do OCR here")
                await self.handle_img_message(message, img)
                return
            else:
                # Remove bot mention from message content, strip leading/trailing whitespace
                cleaned_message = message.content.replace(f'<@!{self.bot.user.id}>', '').strip()
                # Call chat function, with context and cleaned_message
                ctx = await self.bot.get_context(message)
                await self.chat(ctx, message=cleaned_message)
        else:
            # Otherwise, process commands in received message
            await self.bot.process_commands(message)

    """
    function that handles bot interaction in discord if user sent an image message
    :param message: the original message that the user in discord sent to the bot
    :param image: the image that was inside the message that the user sent in discord
    """
    @staticmethod
    async def handle_img_message(message, image):
        # Do more stuff in this func, with chatgpt solving the translated text
        # Calls ocr_image func to extract text from image, and assign to 'text'
        text = ocr_image(image)
        await message.channel.send(f"Converted text: {text}")
        prompt = "Can you solve this math question? "
        prompt += text
        response = await get_gpt_response(prompt)
        await message.channel.send(response)

    """
    Async command function that interacts with GPT AI
    :param ctx: abbreviation for context, an instance of 'commands.Context', provides context around the function call,
                such as ctx.author (user who invoked command), ctx.channel (channel where command was invoked), etc.
    :param *: specifies that arguments after the '*' (i.e., 'message') are passed as keyword arguments, not positional
    :param message: captures remaining content of command as a string
    """
    @staticmethod
    async def chat(ctx, *, message):
        # Create prompt using message content and author's name
        prompt = f"{ctx.author.name}: {message}"
        # calls GPT response using other func, assigns return value to 'response'
        response = await get_gpt_response(prompt)
        # Send the response as a message in the chat
        await ctx.send(f"{ctx.author.mention}, {response}")

    """
    Function that runs the bot (instanced)
    """
    def run(self, token):
        self.bot.run(token)


