import os
import logging
from bot.modules.fs import init
from telegram.ext import Updater


TOKEN = os.environ['TOKEN']
OWNER_ID = os.environ['OWNER_ID']
BASE_DIR = os.getcwd()
url = 'https://eztv.re/'

LOGGER = logging.getLogger(__name__)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

init()
