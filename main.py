import os
from discordbot import DiscordBot

"""
Main function, runs on program start
"""
def main():
    # Get Discord bot key from Windows environment variable
    discord_bot_key = os.environ.get('DISCORD_BOT_KEY')
    # Instantiate instance of discord_bot
    discord_bot = DiscordBot()
    # Run bot, using Discord bot key
    discord_bot.run(discord_bot_key)


# Run main func
if __name__ == "__main__": main()