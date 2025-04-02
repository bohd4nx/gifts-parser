<div align="center">

# 🎁 Telegram Gifts Parser

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-green)](https://docs.aiogram.dev/)
[![PyroFork](https://img.shields.io/badge/PyroFork-2.x-red)](https://github.com/pyrofork/pyrofork)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

</div>

> Telegram bot for scanning chat members and discovering non-upgraded limited gifts (NFT)

<p align="center">
  <a href="README.md">English</a> |
  <a href="./README-RU.md">Русский</a>
</p>

## ✨ Features

- 🔍 **Efficient Chat Scanning** - Process thousands of chat members quickly
- ✨ **Gift Detection** - Find users with limited non-upgraded gifts (NFTs)
- 📊 **Detailed Output** - Get user IDs, usernames, and gift information
- 💾 **Result Exporting** - Save scan results as text files
- 🔄 **Batch Processing** - Process multiple chat links in a single operation
- 🌐 **Multilingual** - Full support for English and Russian interfaces
- 🔄 **Auto-Updates** - Automatically refreshes gift name cache hourly

## 🛠 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bohd4nx/gifts-parser.git
   cd gifts-parser
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings**:
    - Edit `config.ini` with your credentials:
        - Add your Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
        - Set your Telegram API ID and API Hash (from [my.telegram.org](https://my.telegram.org))
        - Enter your phone number for authentication
        - Configure admin user IDs and parsing parameters

## 🚀 Usage

1. **Start the bot**:
   ```bash
   python main.py
   ```

2. **Use the bot**:
    - Send `/start` to the bot
    - Enter a Telegram chat link (or multiple links on separate lines)
    - Wait for scanning to complete
    - Download results using the provided button

## 🔧 Example & Output

**Input Example**:

```
https://t.me/example_group
https://t.me/another_group
```

**Processing Screen**:

```
🔍 Parsing chat [1/2]: @example_group
📊 Total members: 15K
👤 Processed: 10K/15K (67%)
✨ Users found: 42
⌛️ ETA: 5m
```

**Results Format**:

```
@username [12345678]
    Gift Name [gift_id]: 1 | Another Gift [another_id]: 2
```

## 🌟 Advanced Usage

- **Filter specific gifts**: Edit `data/gifts.py` to uncomment the custom gift mappings
- **Change batch size**: Adjust `BATCH_SIZE` in `config.ini` for faster processing (higher values may trigger rate
  limits)
- **Multiple admins**: Add comma-separated user IDs to the `ADMINS` setting

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This project is for educational purposes only. Use responsibly and at your own risk. The developer is not responsible
for any misuse or consequences resulting from the use of this software.

## 🤝 Support

If you find this tool useful:

- ⭐ Star the repository
- 🔄 Share with others
- 📣 Follow [@bohd4nx](https://t.me/bohd4nx) for updates

---

<div align="center">
    <h4>Made with ❤️ by <a href="https://t.me/bohd4nx" target="_blank">@bohd4nx</a></h4>
    <p>Also check <a href="https://t.me/AccessCheckerBot" target="_blank">@AccessCheckerBot</a> & <a href="https://t.me/WhoseGiftBot" target="_blank">@WhoseGiftBot</a></p>
</div>
