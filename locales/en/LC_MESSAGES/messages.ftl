start-text =
    <b>👋 Hello, { $name }!</b>
    
    <b>ℹ️ Telegram Non-Upgraded Gifts Parser</b>
    • Only <b>public groups</b> are supported
    • Groups must have <b>visible member list</b>
    • Private groups are <b>not supported</b>
    • Processing large chats may take time
    
    <b>📝 How to use:</b>
    1. Send a group link (@group or https://t.me/group)
    2. Wait for parsing to complete
    3. Download the results file
    
    <b>💡 Example links:</b>
    • @pavlogradnow_chat
    • @RobloxFleep
    • https://t.me/csgo4at
    
    🔗 <a href="https://github.com/bohd4nx/gifts-parser">Repository</a> • 👨‍💻 <a href="https://t.me/bohd4nx">Developer</a>

parsing-started-large = 
    🔍 <b>Starting advanced parsing:</b> { $chat } | { $total } members

    ℹ️ > The chat has more than 10K members - an enhanced parsing algorithm is being used!

parsing-started = 
    🔍 <b>Starting parse:</b> { $chat } | { $total } members

parsing-complete = 
    ✅ <b>Parsing { $chat } completed!</b>
    
    • <b>Processed:</b> { $total_parsed }/{ $total }
    • <b>Found with gifts:</b> { $total_found }
    • <b>Time elapsed:</b> { $elapsed }

parsing-progress = 
    🔍 <b>Parsing:</b> { $chat }
    
    • <b>Processed:</b> { $parsed }/{ $total }
    • <b>Found with gifts:</b> { $found }
    • <b>ETA:</b> { $elapsed }

cant-get-members = ❌ Could not access { $chat }. Make sure the group is public and link is correct.

hidden-members = ❌ Group { $chat } has hidden member list!

no-results = ❌ No users with non-upgraded gifts found in { $chat }.

btn-russian-selected = • 🇷🇺 Русский •
btn-english-selected = • 🇺🇸 English •
btn-russian = 🇷🇺 Русский
btn-english = 🇺🇸 English

time-format-hours = { $hours }h { $minutes }m
time-format = { $minutes }m { $seconds }s

alert-lang-changed-ru = 🇷🇺 Язык изменён на русский!
alert-lang-changed-en = 🇺🇸 Language changed to English!