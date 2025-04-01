# Movie-Master 🎬✨

![Movie Master Banner](https://img.shields.io/badge/Movie%20Master-Cinema%20Search%20Bot-blueviolet?style=for-the-badge&logo=telegram)  
**The Ultimate Telegram Bot for Movie Junkies!**  
*Search movies like a pro, manage channels/groups, and flex your admin powers—all in one sleek bot!*  

---

## 🌟 What’s This Beast All About?

Yo, welcome to **Movie-Master**! This ain’t your average Telegram bot—it’s a full-on movie-hunting machine built with Python. Whether you’re dying to find details on the latest blockbuster or wanna flex some admin magic, this bot’s got your back. Here’s the lowdown:  

- **IMDb Search**: Type a movie name, actor, or character (like "Batman+Joker"), and boom—title, year, rating, plot, cast, and even a poster link!  
- **Web Search**: Hits up 4 dope websites (Doostihaa, Uptvs, Bigmovies, My-Film) with labeled results. No more guessing where the link’s taking you!  
- **Admin Powers**: Set a custom channel or group (you pick the vibe), broadcast messages to all users, check stats, or wipe logs clean.  
- **Clean AF**: All configs and logs chill in a neat `bot_data` folder—no mess on your desktop!  

This bad boy’s running on `pyTelegramBotAPI` and `IMDbPY`, so it’s legit and smooth as butter. 🧈

---

## 🔥 Features That Slap

| Feature                  | What It Does                                                                 |
|--------------------------|------------------------------------------------------------------------------|
| 🎥 **Movie Search**      | Searches IMDb + 4 sites and drops results with clickable buttons.           |
| 📣 **Broadcast**         | Admin can spam (nicely) all users with a single message.                    |
| 🎙️ **Channel/Group**     | Set a custom name and link—choose if it’s a channel or group, no guessing!  |
| 📊 **Stats**             | See how many peeps are using your bot.                                      |
| 🗑️ **Clear Logs**        | Wipe the slate clean when logs get too chunky.                              |
| 🗂️ **Organized Files**   | Everything’s tucked into `bot_data/`—no clutter!                            |

---

## 🛠️ How to Get This Party Started

Let’s fire this thing up! Here’s the step-by-step to get **Movie-Master** rolling on your machine.  

### 📋 Prerequisites
- **Python 3.7+**: Make sure you’ve got Python installed (check with `python3 --version`).  
- **pip**: For grabbing the goodies we need.  
- **Telegram Bot Token**: Hit up [BotFather](https://t.me/BotFather) on Telegram and snag a token.  
- **Your Admin ID**: Your Telegram user ID (numeric, grab it from a bot like `@userinfobot`).  

### ⚙️ Installation
1. **Clone the Repo**  
   ```bash
   git clone https://github.com/MasterShayan/Movie-Master.git
   cd Movie-Master
   ```

2. **Set Up a Virtual Environment (Optional but Cool)**  
   ```bash
   python3 -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate     # Windows
   ```

3. **Install the Dependencies**  
   ```bash
   pip install pyTelegramBotAPI IMDbPY
   ```

4. **Tweak the Code**  
   Open `q.py` (or whatever you name it) and swap these placeholders:  
   - `YOUR_BOT_TOKEN_HERE` → Your bot token from BotFather.  
   - `YOUR_ADMIN_ID_HERE` → Your numeric Telegram ID.  

   Example:
   ```python
   API_TOKEN = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
   ADMIN_ID = '123456789'
   ```

5. **Run That Baby**  
   ```bash
   python3 q.py
   ```
   If you see logs like `Bot started.` in `bot_data/bot.log`, you’re golden! 🌟

---

## 🎮 How to Use It

- **Normal Users**:  
  - `/start`: Get a welcome message with the channel/group link.  
  - Type anything (e.g., "Inception"): Get IMDb details + search results from 4 sites.  

- **Admin Mode**:  
  - `/panel`: Opens the admin menu.  
    - **Stats**: Check user count.  
    - **Broadcast**: Send a message to everyone.  
    - **Set Channel/Group**: Name → Link → Pick "Channel" or "Group".  
    - **User List**: See all user IDs.  
    - **Clear Logs**: Reset the log file.  

---

## 📂 File Structure

Here’s what you’ll see after running:  
```
Movie-Master/
├── q.py              # The main bot script
├── bot_data/         # Where all the magic lives
│   ├── channel_data.json  # Channel/Group info
│   ├── users.txt         # User IDs
│   ├── members.txt       # Member IDs
│   ├── panel.txt         # Admin panel state
│   ├── bot.log           # Logs (errors, info, etc.)
│   └── temp_channel_name.txt  # Temp file during setup (gets deleted)
└── README.md         # This dope file you’re reading
```

---

## 🛡️ License

This project’s rocking the **Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)** license. What’s that mean?  
- **Give Credit**: Mention me (MasterShayan) if you share it.  
- **No Commercial Use**: Don’t make money off this—keep it free vibes!  
- **No Mods**: Share it as-is, no remixing allowed.  

Check the full deets [here](https://creativecommons.org/licenses/by-nc-nd/4.0/).  

---

## 🤓 Pro Tips

- **Debugging**: Check `bot_data/bot.log` if shit hits the fan.  
- **Rate Limits**: Telegram’s picky—don’t spam too hard or you’ll get a timeout.  
- **IMDb**: Sometimes slow—give it a sec if results lag.  

---

## 🌌 Why This Bot Rules

**Movie-Master** isn’t just a bot—it’s your cinema sidekick. Built from scratch to be fast, clean, and badass, it’s perfect for movie buffs and Telegram tinkerers alike. Push it to GitHub, flex it with your crew, and watch it shine! ✨  

Got ideas to make it crazier? Hit me up on GitHub issues—I’m all ears!  

---

**Made with 💪 by [MasterShayan](https://github.com/MasterShayan)**  
