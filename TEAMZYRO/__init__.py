from TEAMZYRO.core.bot import ZYRO
from TEAMZYRO.core.dir import dirr
from TEAMZYRO.core.git import git
from TEAMZYRO.core.userbot import Userbot
from TEAMZYRO.misc import dbb, heroku
from SafoneAPI import SafoneAPI
from .logging import LOGGER
from .platforms import (
    AppleAPI,
    CarbonAPI,
    SoundAPI,
    SpotifyAPI,
    RessoAPI,
    TeleAPI,
    YouTubeAPI,
)

# -------------------------- INITIAL SETUP -------------------------------

dirr()
git()
dbb()
heroku()

# -------------------------- MAIN CLIENTS --------------------------------

app = ZYRO()
api = SafoneAPI()
userbot = Userbot()
# application = application   # (Disabled for now)

# -------------------------- PLATFORM APIS -------------------------------

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

# --------------------------- GLOBAL STATE -------------------------------

locks = {}
message_counters = {}
spam_counters = {}
last_characters = {}
sent_characters = {}
first_correct_guesses = {}
message_counts = {}
last_user = {}
warned_users = {}
user_cooldowns = {}
user_nguess_progress = {}
user_guess_progress = {}

# -------------------------- POWER SETUP --------------------------------
