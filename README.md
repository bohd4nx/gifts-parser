<div align="center">

# 🎁 Telegram Gifts Parser

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-green)](https://docs.aiogram.dev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Telegram%20Bot-lightgrey)](https://github.com/bohd4nx/gift-parser)

</div>

> Search for users with non-upgraded limited gifts in chats.

<p align="center">
  <a href="README.md">English</a> |
  <a href="./README-RU.md">Русский</a>
</p>

## 📱 Screenshots

<details>
<summary>Click to expand</summary>

### Main

![image](https://github.com/user-attachments/assets/f8259282-15cf-4b47-bcc7-0eca6208b854)

### Result

![image](https://github.com/user-attachments/assets/6c29656d-43a2-4862-89ec-7d922603bde0)

</details>

## ✨ Features

- 🔍 Automatic Telegram chat scanning
- ✨ Detection of limited, non-upgraded gifts (NFT)
- 📊 Collection of user profiles and gift IDs
- 💾 Saving scan results

## 🛠 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bohd4nx/gifts-parser.git
   cd gifts-parser
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Edit config.ini in the project root directory to match your needs.

## 🚀 Usage

1. Start the bot:
   ```bash
   python main.py
   ```
2. Send the bot a /start command and follow the instructions:
    - Provide a Telegram chat link (e.g., https://t.me/somechat)
    - Wait for the bot to parse the chat
    - Use the bot’s commands to fetch results

## 🔧 Example Usage & Output

1. Send the '/start' command to the bot.
2. The bot will ask for a Telegram chat link (e.g., https://t.me/samplechat).
3. Bot starts parsing and shows progress updates:
   ```
   🔍 Parsing chat: @samplechat
   📊 Total members: 150
   ⏳ Parsed: 10/150
   ✨ Found users: 2
   ```
4. After finishing, the bot offers a download of the results:
   ```
   ✅ Parse completed for @samplechat!
   📊 Total members: 150
   ⏳ Parsed: 150/150
   ✨ Found users: 15

   [ Download Results ]
   ```
5. Clicking “Download Results” gives you a file with usernames and their limited gift info.

## 📝 License

This project is MIT licensed. See LICENSE for more information.

## 🌟 Support

If you find this project useful:

- Give it a star ⭐
- Share with others 🔄
- Consider contributing 🛠️

---

<div align="center">
    <h4>Built with ❤️ by <a href="https://t.me/bohd4nx" target="_blank">Bohdan</a></h4>
</div>
