start-text =
    <b>👋 Привет, { $name }!</b>
    
    <b>ℹ️ Парсер неулучшенных подарков Telegram</b>
    • Поддерживаются только <b>публичные группы</b>
    • У группы должен быть <b>видимый список участников</b>
    • Приватные группы <b>не поддерживаются</b>
    • Обработка больших чатов может занять время  
    
    <b>📝 Как использовать:</b>
    1. Отправьте ссылку на группу (@group or https://t.me/group)
    2. Дождитесь завершения парсинга
    3. Скачайте файл с результатами
    
    <b>💡 Примеры ссылок:</b>
    • @pavlogradnow_chat
    • @RobloxFleep
    • https://t.me/csgo4at
    
    🔗 <a href="https://github.com/bohd4nx/gifts-parser">Репозиторий</a> • 👨‍💻 <a href="https://t.me/bohd4nx">Разработчик</a>

parsing-started-large = 
    🔍 <b>Начинаю расширенный парсинг:</b> { $chat } | { $total } участников

    ℹ️ > В чате больше 10к участников, используется улучшенный алгоритм!

parsing-started = 
    🔍 <b>Начинаю парсинг:</b> { $chat } | { $total } участников

parsing-complete = 
    ✅ <b>Парсинг { $chat } завершён!</b>  

    • <b>Обработано:</b> { $total_parsed }/{ $total }
    • <b>Найдено с подарками:</b> { $total_found }  
    • <b>Время выполнения:</b> { $elapsed }

parsing-progress = 
    🔍 <b>Парсинг:</b> { $chat }
    
    • <b>Обработано:</b> { $parsed }/{ $total }
    • <b>Найдено с подарками:</b> { $found }  
    • <b>ETA:</b> { $elapsed }

cant-get-members = ❌ Не удалось получить доступ к { $chat }. Убедитесь, что группа публичная и ссылка корректна.

hidden-members = ❌ У группы { $chat } скрыт список участников!

no-results = ❌ Пользователи с неулучшенными подарками не найдены в { $chat }.

btn-russian-selected = • 🇷🇺 Русский •
btn-english-selected = • 🇺🇸 English •
btn-russian = 🇷🇺 Русский
btn-english = 🇺🇸 English

time-format-hours = { $hours }ч { $minutes }м
time-format = { $minutes }м { $seconds }с

alert-lang-changed-ru = 🇷🇺 Язык изменён на русский!
alert-lang-changed-en = 🇺🇸 Language changed to English!