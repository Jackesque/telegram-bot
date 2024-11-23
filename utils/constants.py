import os

from country_list import countries_for_language
from dotenv import load_dotenv
from telegram import InlineKeyboardButton

load_dotenv()

TOKEN = os.getenv("TOKEN")
USERS_DATA_PATH = "./output/users_data.xlsx"

USERS_DATA_COLUMNS = [
    "Timestamp",
    "User Id",
    "Username",
    "First Name",
    "Last Name",
    "Country",
    "Phone Number",
    "Broker UID",
    "Broker Full Name",
    "Account Balance (USD)",
    "Email (for VIP invitation)",
]

COUNTRIES = [country[1] for country in countries_for_language("en")]
COUNTRIES = [country for country in COUNTRIES if country]

PLATFORMS = ["KCM", "Dooprime"]

PLATFORMS_KEYBOARD = InlineKeyboardButton(
    [[InlineKeyboardButton(platform, callback_data=platform) for platform in PLATFORMS]]
)

# Links (not provided)
ACCOUNT_LINK = "https://example.com"

# Guide image path (not provided)
GUIDE_IMAGE_PATH = "ONE.jpg"
