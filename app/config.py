from environs import Env

env = Env()
env.read_env()

API_KEY = env.str('API_KEY')
BOT_TOKEN = env.str('BOT_TOKEN')
SKIP_UPDATES = env.bool('SKIP_UPDATE', True)
ADMIN_IDS = env.list('ADMIN_IDS')
ID_CHANNEL = env.str('ID_CHANNEL')
# ID_CHANNEL = 42372693
