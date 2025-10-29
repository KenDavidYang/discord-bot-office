import os
from dotenv import load_dotenv

# ----------- ENVIRONMENT VARIABLES -----------

load_dotenv()
TOKEN = os.getenv('TOKEN')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# ----------- DISCORD -----------

GUILDS = {
    "default_marketing_server": 1391989364602437802
}
CHANNELS = {
    "general": 1391989365336707174,
    "cookies": 1391989487629893632,
    "trivia": 1391989523272957982,
    "memes": 1392342028985307289,
    "cats":1394132597587574965
}
STICKERS = {
    "nervous_cat": 823976102976290866
}

# ----------- OTHER -----------

ERROR_MESSAGES = ("What", "🤨", "yep, that's an error", "pardon?", "wym", "idk what you meant",
                  "typo?", "wait, what?", "yo, stop playing with me. I don't like errors. Type properly like a civilized person",
                   "Add this to your list of errors:", "If this isn't a user error, it's not my fault either. Add 1 to the dev's headache counter",
                    "What was that? I coudln't quite hear you", "I don't understand", "もうわからん" 
                )