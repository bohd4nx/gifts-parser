<h1 align="center">🎁 Telegram Gifts Parser Bot</h1>

<p align="center">
   <b>Advanced parser for extracting non-upgraded gifts from Telegram users in public groups and supergroups.</b>
</p>

<div align="center">

![Bot Demo](https://github.com/user-attachments/assets/3774232e-426b-4f77-aa01-119675835c58)

[Report Bug](https://github.com/bohd4nx/gifts-parser/issues) · [Request Feature](https://github.com/bohd4nx/gifts-parser/issues)

</div>

## ✨ Features

- 🎯 **Non-Upgraded Gift Parsing** - Extract and analyze non-upgraded gifts from users in Telegram groups
- 🔍 **Smart Member Detection** - Automatically checks member list visibility and filters **only real participants**
- 🚀 **Dual Algorithm System** - Optimized parsing for both regular groups and large supergroups (11K+ members)
- 🌍 **Multi-Language Support** - Full English and Russian localization with inline keyboard switching
- 📄 **Detailed Export** - Download parsed data as organized text files with timestamps
- ⚡ **Real-Time Progress** - Live updates with ETA calculations and processing statistics

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- Telegram account with API credentials
- Bot token from [@BotFather](https://t.me/BotFather)

### 2. Installation

```bash
git clone https://github.com/bohd4nx/gifts-parser.git
cd gifts-parser
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration

Copy example configuration and edit:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
# Get token from @BotFather
BOT_TOKEN=your_bot_token_here

# Get API credentials from https://my.telegram.org/apps
API_ID=your_api_id
API_HASH=your_api_hash

# Your Telegram phone number (with country code)
PHONE_NUMBER=+1234567890
```

### 4. Getting Telegram API Credentials

1. Visit [https://my.telegram.org/apps](https://my.telegram.org/apps)
2. Login with your Telegram account
3. Create a new application
4. Copy `API_ID` and `API_HASH` to your `.env` file

### 5. Run

```bash
python main.py
```

## 📱 Usage

### Bot Commands

- `/start` - Start the bot and see welcome message
- Language switching via inline keyboard (🇺🇸 English / 🇷🇺 Русский)

### Parsing Groups

Send any of these formats to the bot:

```
@pavlogradnow_chat
@RobloxFleep
https://t.me/csgo4at
```

### Supported Group Types

| Group Type             | Supported | Requirements                          |
| ---------------------- | --------- | ------------------------------------- |
| **Public Groups**      | ✅        | Visible member list required          |
| **Public Supergroups** | ✅        | Must have accessible participant list |
| **Private Groups**     | ❌        | Not supported                         |

### Parsing Process

1. **Input Validation** - Bot automatically verifies group accessibility and member list visibility
2. **Member Filtering** - Smart detection excludes bots and deleted users, etc
3. **Algorithm Selection** - Automatically chooses optimal parsing method based on group size
4. **Real-Time Updates** - Live progress tracking with ETA calculations and found gift statistics
5. **Results Export** - Download comprehensive statistics as formatted text file

## 🐛 Troubleshooting

### Common Issues

**Parsing fails:**

- Ensure group is public with visible member list
- Check if group link is correct format
- Verify API credentials are valid

**Session errors:**

- Delete `.session` files and restart
- Re-enter phone number verification

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center">

### Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

**Star ⭐ this repo if you found it useful!**

</div>
