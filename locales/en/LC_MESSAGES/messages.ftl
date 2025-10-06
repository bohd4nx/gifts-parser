start-text =
    <b>👋 Hello, { $name }!</b>
    
    <b>ℹ️ Telegram Non-Upgraded Gifts Parser</b>
    • Only <b>public groups</b> are supported
    • Groups must have <b>visible member list</b>
    • Private groups are <b>not supported</b>
    • Processing large chats may take time
    
    <b>📝 How to use:</b>
    1. Send a group link (@groupname or https://t.me/groupname)
    2. Wait for parsing to complete
    3. Download the results file
    
    <b>🚀 Send me a group link!</b>

parsing-started = 
    🔍 <b>Starting parse:</b> { $chat } | { $total } members

parsing-started-large = 
    🔍 <b>Starting advanced parsing:</b> { $chat } | { $total } members

    ℹ️ > The chat has more than 10K members - an enhanced parsing algorithm is being used!

parsing-progress = 
    🔍 <b>Parsing:</b> { $chat }
    
    • <b>Processed:</b> { $parsed }/{ $total }
    • <b>Found with gifts:</b> { $found }
    • <b>ETA:</b> { $elapsed }

parsing-complete = 
    ✅ <b>Parsing { $chat } completed!</b>
    
    • <b>Processed:</b> { $total_parsed }/{ $total }
    • <b>Found with gifts:</b> { $total_found }
    • <b>Time elapsed:</b> { $elapsed }

no-results = ❌ No users with non-upgraded gifts found in { $chat }.

hidden-members = ❌ Group { $chat } has hidden member list!
cant-get-members = ❌ Could not access { $chat }. Make sure the group is public and link is correct.

time-format = { $minutes }m { $seconds }s
time-format-hours = { $hours }h { $minutes }m