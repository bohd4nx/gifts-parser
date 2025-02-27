<div align="center">

# 🎁 Telegram Gifts Parser

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-green)](https://docs.aiogram.dev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]
[![Platform](https://img.shields.io/badge/Telegram%20Bot-lightgrey)](https://github.com/bohd4nx/gift-parser)

</div>

> Автоматический поиск невыпущенных (неапгрейженных) лимитированных подарков в Telegram-чатах.

<p align="center">
  <a href="README.md">English</a> |
  <a href="./README-RU.md">Русский</a>
</p>

## 📱 Скриншоты

<details>
<summary>Нажмите, чтобы развернуть</summary>

### Бот

![image](https://github.com/user-attachments/assets/f8259282-15cf-4b47-bcc7-0eca6208b854)

### Результаты

![image](https://github.com/user-attachments/assets/6ee51145-8a82-4f34-9323-84b0b81ddd72)

</details>

## ✨ Возможности

- 🔍 Автоматическое сканирование Telegram-чата
- ✨ Обнаружение лимитированных подарков (NFT), которые ещё не были апгрейжены
- 📊 Сбор данных о пользователях и их подарках
- 💾 Сохранение результатов сканирования
- 🔄 Возможность обработки нескольких ссылок на чаты
- 🌐 Мультиязычный интерфейс (русский и английский)
- 🔄 Автоматическое обновление кэша названий подарков

## 🛠 Установка

1. Клонируйте репозиторий: (или просто скачайте архивом)

   ```bash
   git clone https://github.com/bohd4nx/gifts-parser.git
   cd gifts-parser
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Отредактируйте файл config.ini в корне проекта:
   - Укажите ваш токен бота
   - Укажите Telegram API ID и API Hash
   - Добавьте номер телефона в международном формате
   - Настройте администраторов и параметры парсинга

## 🚀 Использование

1. Запустите бота:
   ```bash
   python main.py
   ```
2. Отправьте боту команду /start и следуйте инструкциям:
   - Предоставьте ссылку на Telegram-чат (например, https://t.me/somechat)
   - Для пакетной обработки отправьте несколько ссылок, разделенных переносами строк
   - Дождитесь окончания сканирования чата(ов)
   - Используйте кнопку загрузки для получения результатов

## 🔧 Пример и вывод

1. Отправьте боту команду «/start».
2. Бот запросит ссылку на чат или несколько ссылок:

   ```
   https://t.me/samplechat
   https://t.me/anotherchat
   ```

3. Бот начнёт парсинг каждого чата поочередно и будет показывать прогресс:
   ```
   🔍 Парсинг чата [1/3]: @samplechat
   📊 Всего участников: 15K
   👤 Обработано: 10K/15K
   ✨ Найдено пользователей: 9.1K
   ⌛️ Осталось примерно: 1ч 33м
   ```

4. После завершения всех чатов бот предложит скачать результаты для каждого из них:

## 📝 Лицензия

Проект распространяется по лицензии MIT. Подробнее см. LICENSE.

## 🌟 Поддержка

Если вам понравился проект:

- Поставьте звезду ⭐
- Поделитесь с друзьями 🔄

---

<div align="center">
    <h4>Built with ❤️ by <a href="https://t.me/bohd4nx" target="_blank">Bohdan</a></h4>
</div>
