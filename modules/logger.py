import logging
import logging.handlers
from nextcord.ext import commands

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.setup_logging()

    def setup_logging(self):
        log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)

        # Get root logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(console_handler)

        # Silence some noisy loggers
        logging.getLogger('nextcord').setLevel(logging.WARNING)
        logging.getLogger('nextcord.gateway').setLevel(logging.WARNING)
        logging.getLogger('nextcord.http').setLevel(logging.WARNING)

        print("Logger setup complete.")

def setup(bot):
    bot.add_cog(Logger(bot))