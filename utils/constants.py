import os

from country_list import countries_for_language
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

TOKEN = os.getenv("TOKEN")
USERS_DATA_PATH = "./output/users_data.xlsx"
USERS_DATA_PATH_VI = "./output/Dữ liệu người dùng.xlsx"

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

USERS_DATA_COLUMNS_VI = [
    "Thời gian",
    "Id người dùng",
    "Username",
    "Tên",
    "Họ",
    "Quốc gia",
    "SĐT",
    # "Broker UID",
    # "Broker Full Name",
    "Số tiền gửi (VND)",
    # "Email (for VIP invitation)",
]

COUNTRIES = [country[1] for country in countries_for_language("en")]
COUNTRIES = [country for country in COUNTRIES if country]

PLATFORMS = ["KCM", "Dooprime"]

PLATFORMS_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton(platform, callback_data=platform) for platform in PLATFORMS]]
)

# Links
ACCOUNT_LINK = "https://my.dooprime.com/vi/links/go/47570"

# Guide image directory path
GUIDE_OPEN_ACCOUNT_DIRECTORY_PATH = "input/KCMTrade Open Account Guide"
GUIDE_DEPOSIT_WITHDRAW_DIRECTORY_PATH = "input/KCMTrade Deposit and Withdraw Guide"
GUIDE_DEPOSIT_DIRECTORY_PATH = os.path.join(
    GUIDE_DEPOSIT_WITHDRAW_DIRECTORY_PATH, "deposit"
)
GUIDE_WITHDRAW_DIRECTORY_PATH = os.path.join(
    GUIDE_DEPOSIT_WITHDRAW_DIRECTORY_PATH, "withdraw"
)
