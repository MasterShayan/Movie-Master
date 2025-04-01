import telebot
import os
import logging
import json
from typing import List, Optional
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from imdb import IMDb
import time

API_TOKEN = '8145228120:AAGsyGwHdu7NQ_NS6MorcHK9QLkpT0xemMY'
ADMIN_ID = '5047811078'
DATA_DIR = 'bot_data'
CHANNEL_DATA_FILE = os.path.join(DATA_DIR, 'channel_data.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
MEMBERS_FILE = os.path.join(DATA_DIR, 'members.txt')
PANEL_FILE = os.path.join(DATA_DIR, 'panel.txt')
LOG_FILE = os.path.join(DATA_DIR, 'bot.log')
TEMP_CHANNEL_NAME_FILE = os.path.join(DATA_DIR, 'temp_channel_name.txt')

os.makedirs(DATA_DIR, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

ia = IMDb()
bot = telebot.TeleBot(API_TOKEN)

def ensure_directory_and_file(file_path: str, default_content: str = '') -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(default_content)
        logger.info(f"Created missing file: {file_path}")

def read_file(file_path: str) -> List[str]:
    ensure_directory_and_file(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return []

def write_file(file_path: str, content: str, mode: str = 'a') -> None:
    ensure_directory_and_file(file_path)
    try:
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(content + '\n')
    except Exception as e:
        logger.error(f"Error writing to {file_path}: {e}")

def get_channel_data() -> dict:
    default_data = {"name": "DefaultChannel", "link": "https://t.me/DefaultChannel", "type": "Channel"}
    ensure_directory_and_file(CHANNEL_DATA_FILE, json.dumps(default_data))
    try:
        with open(CHANNEL_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict) or "name" not in data or "link" not in data or "type" not in data:
                logger.warning("Invalid channel data format. Resetting to default.")
                set_channel_data(default_data["name"], default_data["link"], default_data["type"])
                return default_data
            return data
    except (json.JSONDecodeError, Exception) as e:
        logger.error(f"Error reading channel data: {e}. Using default.")
        set_channel_data(default_data["name"], default_data["link"], default_data["type"])
        return default_data

def set_channel_data(name: str, link: str, link_type: str) -> None:
    data = {"name": name, "link": link, "type": link_type}
    try:
        with open(CHANNEL_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(f"Error writing channel data: {e}")

def is_admin(user_id: int) -> bool:
    return user_id == int(ADMIN_ID)

def search_imdb(query: str) -> Optional[dict]:
    try:
        movies = ia.search_movie(query)
        if not movies:
            return None
        movie = movies[0]
        ia.update(movie)
        return {
            'title': movie.get('title', 'N/A'),
            'year': str(movie.get('year', 'N/A')),
            'rating': str(movie.get('rating', 'N/A')),
            'plot': movie.get('plot outline', 'No plot available'),
            'cast': ', '.join([str(actor) for actor in movie.get('cast', [])[:5]]) or 'N/A',
            'poster': movie.get('full-size cover url', 'No poster available')
        }
    except Exception as e:
        logger.error(f"IMDb search error: {e}")
        return None

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    members = read_file(MEMBERS_FILE)
    if str(chat_id) not in members:
        write_file(MEMBERS_FILE, str(chat_id))
        write_file(USERS_FILE, str(chat_id))
    
    try:
        channel_data = get_channel_data()
        markup = InlineKeyboardMarkup()
        button_text = f"Visit {channel_data['type']}"
        markup.add(InlineKeyboardButton(button_text, url=channel_data['link']))
        welcome_text = (
            "Welcome to the Ultimate Movie Search Bot!\n"
            "Search for movies, actors, or characters (e.g., 'Batman+Joker').\n"
            "Features: IMDb search, custom channel/group, admin tools, and more!\n"
            f"{button_text}: @{channel_data['name']}"
        )
        bot.reply_to(message, welcome_text, reply_markup=markup, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Error in handle_start: {e}")
        bot.reply_to(message, "An error occurred. Please try again later.")

@bot.message_handler(commands=['panel'])
def handle_panel(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "Access denied: Admin only!")
        return
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Stats"), KeyboardButton("Broadcast"))
    markup.add(KeyboardButton("Set Channel/Group"), KeyboardButton("User List"))
    markup.add(KeyboardButton("Clear Logs"))
    bot.reply_to(message, "Admin Panel:\nChoose an option:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "Stats")
def handle_stats(message):
    if not is_admin(message.from_user.id):
        return
    members = read_file(MEMBERS_FILE)
    member_count = len(set(members))
    bot.reply_to(message, f"Total users: {member_count}")

@bot.message_handler(func=lambda m: m.text == "Broadcast")
def handle_broadcast(message):
    if not is_admin(message.from_user.id):
        return
    write_file(PANEL_FILE, "Broadcast", mode='w')
    bot.reply_to(message, "Send the message to broadcast to all users:")

@bot.message_handler(func=lambda m: m.text == "Set Channel/Group")
def handle_set_channel(message):
    if not is_admin(message.from_user.id):
        return
    write_file(PANEL_FILE, "SetChannelName", mode='w')
    bot.reply_to(message, "Enter the name of the channel or group (e.g., MyChannel):")

@bot.message_handler(func=lambda m: m.text == "User List")
def handle_user_list(message):
    if not is_admin(message.from_user.id):
        return
    users = read_file(USERS_FILE)
    bot.reply_to(message, f"Users:\n{', '.join(users) if users else 'No users yet.'}")

@bot.message_handler(func=lambda m: m.text == "Clear Logs")
def handle_clear_logs(message):
    if not is_admin(message.from_user.id):
        return
    write_file(LOG_FILE, '', mode='w')
    bot.reply_to(message, "Logs cleared successfully.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    panel_status = read_file(PANEL_FILE)[0] if read_file(PANEL_FILE) else "none"
    
    if panel_status == "Broadcast" and is_admin(user_id):
        write_file(PANEL_FILE, "none", mode='w')
        users = read_file(USERS_FILE)
        for user in users:
            try:
                bot.send_message(user, text, parse_mode='HTML')
            except Exception as e:
                logger.error(f"Failed to send to {user}: {e}")
        bot.reply_to(message, "Broadcast sent successfully.")
        return
    
    if panel_status == "SetChannelName" and is_admin(user_id):
        write_file(PANEL_FILE, "SetChannelLink", mode='w')
        bot.reply_to(message, f"Name set to '{text}'. Now send the join link (e.g., https://t.me/+abc123):")
        write_file(TEMP_CHANNEL_NAME_FILE, text, mode='w')
        return
    
    if panel_status == "SetChannelLink" and is_admin(user_id):
        channel_name = read_file(TEMP_CHANNEL_NAME_FILE)[0] if read_file(TEMP_CHANNEL_NAME_FILE) else "Unnamed"
        write_file(PANEL_FILE, "SetChannelType", mode='w')
        write_file(TEMP_CHANNEL_NAME_FILE, f"{channel_name}\n{text}", mode='w')
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("Channel"), KeyboardButton("Group"))
        bot.reply_to(message, "Is this a Channel or Group? Select one:", reply_markup=markup)
        return
    
    if panel_status == "SetChannelType" and is_admin(user_id) and text in ["Channel", "Group"]:
        temp_data = read_file(TEMP_CHANNEL_NAME_FILE)
        channel_name = temp_data[0] if len(temp_data) > 0 else "Unnamed"
        channel_link = temp_data[1] if len(temp_data) > 1 else "https://t.me/DefaultChannel"
        set_channel_data(channel_name, channel_link, text)
        write_file(PANEL_FILE, "none", mode='w')
        button_text = f"Visit {text}"
        bot.reply_to(message, f"{button_text} updated to: @{channel_name} ({channel_link})")
        if os.path.exists(TEMP_CHANNEL_NAME_FILE):
            os.remove(TEMP_CHANNEL_NAME_FILE)
        return
    
    admin_commands = ["Stats", "Broadcast", "Set Channel/Group", "User List", "Clear Logs", "Channel", "Group"]
    if text in admin_commands:
        return
    
    imdb_result = search_imdb(text)
    if imdb_result:
        imdb_text = (
            f"<b>{imdb_result['title']} ({imdb_result['year']})</b>\n"
            f"Rating: {imdb_result['rating']}\n"
            f"Cast: {imdb_result['cast']}\n"
            f"Plot: {imdb_result['plot']}"
        )
        markup = InlineKeyboardMarkup()
        if imdb_result['poster'] != 'No poster available':
            markup.add(InlineKeyboardButton("View Poster", url=imdb_result['poster']))
        try:
            bot.reply_to(message, imdb_text, reply_markup=markup, parse_mode='HTML')
        except Exception as e:
            logger.error(f"Error sending IMDb result: {e}")
    
    channel_data = get_channel_data()
    markup = InlineKeyboardMarkup()
    search_urls = [
        ("Doostihaa", f"http://www.doostihaa.com/?s={text}&btnSubmit="),
        ("Uptvs", f"http://www.uptvs.com/?blogs=1%2C5&s={text}"),
        ("Bigmovies", f"http://www.bigmovies.ir/?s={text}"),
        ("My-Film", f"http://my-film.in/?s={text}")
    ]
    for site_name, url in search_urls:
        markup.add(InlineKeyboardButton(f"View Results - {site_name}", url=url))
    
    try:
        bot.reply_to(message, "Search results from 4 websites + IMDb:", reply_markup=markup)
    except Exception as e:
        logger.error(f"Error sending search results: {e}")

def main():
    for file in [CHANNEL_DATA_FILE, USERS_FILE, MEMBERS_FILE, PANEL_FILE, LOG_FILE]:
        ensure_directory_and_file(file)
    
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Start the bot"),
        telebot.types.BotCommand("/panel", "Admin panel (admin only)")
    ])
    
    logger.info("Bot started.")
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            logger.error(f"Polling error: {e}")
            try:
                bot.send_message(ADMIN_ID, f"Bot crashed: {e}")
            except:
                pass
            time.sleep(5)

if __name__ == "__main__":
    main()
