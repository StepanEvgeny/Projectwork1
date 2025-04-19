from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from logic import get_schedule_for_day, get_week_schedule, add_lesson, delete_lesson_by_id

# === НАСТРОЙКИ ===
TOKEN = '8109824187:AAGrAjqoeFpkJyXSlva8u5-HVH0qZTmmtZk'
ADMIN_ID = 7048073193  # замени на свой Telegram ID

# === МНОГОЯЗЫЧНОСТЬ ===
phrases = {
    'start': {
        'ru': "Привет! Я бот онлайн-школы 👋\nНажми кнопку ниже, чтобы выбрать день недели:",
        'en': "Hi! I'm the online school bot 👋\nClick the button below to choose a day:"
    },
    'help': {
        'ru': (
            "/start — Главное меню\n"
            "/week — Расписание на неделю\n"
            "/add <день> <время> <предмет> — Добавить урок (админ)\n"
            "/delete <id> — Удалить урок по ID (админ)\n"
            "/lang ru/en — Сменить язык\n"
            "/help — Помощь"
        ),
        'en': (
            "/start — Main menu\n"
            "/week — Weekly schedule\n"
            "/add <day> <time> <subject> — Add lesson (admin)\n"
            "/delete <id> — Delete lesson by ID (admin)\n"
            "/lang ru/en — Change language\n"
            "/help — Help"
        )
    },
    'choose_day': {'ru': "Выбери день недели:", 'en': "Choose a day of the week:"},
    'main_menu': {'ru': "🔝 Главное меню:\nНажми кнопку, чтобы выбрать день:", 'en': "🔝 Main menu:\nClick the button to choose a day:"},
    'only_admin_add': {'ru': "⛔ Только администратор может добавлять занятия.", 'en': "⛔ Only the administrator can add lessons."},
    'only_admin_delete': {'ru': "⛔ Только администратор может удалять занятия.", 'en': "⛔ Only the administrator can delete lessons."},
    'add_format_error': {'ru': "❗ Используй формат: /add Понедельник 10:00 Математика", 'en': "❗ Use format: /add Monday 10:00 Math"},
    'delete_format_error': {'ru': "❗ Используй формат: /delete <id>", 'en': "❗ Use format: /delete <id>"},
    'language_set': {'ru': "Язык установлен: ru", 'en': "Language set: en"},
    'language_hint': {'ru': "Укажи язык: /lang ru или /lang en", 'en': "Please specify the language: /lang ru or /lang en"},
    'back': {'ru': "🔙 Назад", 'en': "🔙 Back"},
    'home': {'ru': "🏠 Главное меню", 'en': "🏠 Main menu"},
    'view_schedule': {'ru': "📅 Посмотреть расписание", 'en': "📅 View schedule"},
}

user_lang = {}

day_translations = {
    'Понедельник': 'Monday',
    'Вторник': 'Tuesday',
    'Среда': 'Wednesday',
    'Четверг': 'Thursday',
    'Пятница': 'Friday',
    'Суббота': 'Saturday',
    'Воскресенье': 'Sunday',
    'Monday': 'Понедельник',
    'Tuesday': 'Вторник',
    'Wednesday': 'Среда',
    'Thursday': 'Четверг',
    'Friday': 'Пятница',
    'Saturday': 'Суббота',
    'Sunday': 'Воскресенье',
}

def _(user_id, key):
    lang = user_lang.get(user_id, 'ru')
    return phrases.get(key, {}).get(lang, key)

# === ХЕНДЛЕРЫ ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_lang[update.effective_user.id] = 'ru'
    keyboard = [[InlineKeyboardButton(_(update.effective_user.id, 'view_schedule'), callback_data='choose_day')]]
    await update.message.reply_text(_(update.effective_user.id, 'start'), reply_markup=InlineKeyboardMarkup(keyboard))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(_(update.effective_user.id, 'help'))

async def week_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_week_schedule(), parse_mode='Markdown')

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args and context.args[0] in ['ru', 'en']:
        user_lang[update.effective_user.id] = context.args[0]
        await update.message.reply_text(_(update.effective_user.id, 'language_set'))
    else:
        await update.message.reply_text(_(update.effective_user.id, 'language_hint'))

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(_(update.effective_user.id, 'only_admin_add'))
        return
    try:
        day_input = context.args[0]
        day = day_translations.get(day_input, day_input)
        time, subject = context.args[1], " ".join(context.args[2:])
        msg = add_lesson(day, time, subject)
        await update.message.reply_text(msg)
    except:
        await update.message.reply_text(_(update.effective_user.id, 'add_format_error'))

async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(_(update.effective_user.id, 'only_admin_delete'))
        return
    try:
        lesson_id = int(context.args[0])
        msg = delete_lesson_by_id(lesson_id)
        await update.message.reply_text(msg)
    except:
        await update.message.reply_text(_(update.effective_user.id, 'delete_format_error'))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == 'choose_day':
        ru_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        days_keyboard = [
            [InlineKeyboardButton(f"🗓 {day_translations[day] if user_lang.get(user_id) == 'en' else day}", callback_data=f'day_{day}')]
            for day in ru_days
        ]
        days_keyboard.append([InlineKeyboardButton(_(user_id, 'home'), callback_data='main_menu')])
        await query.edit_message_text(_(user_id, 'choose_day'), reply_markup=InlineKeyboardMarkup(days_keyboard))

    elif query.data.startswith('day_'):
        day = query.data.split('_')[1]
        schedule = get_schedule_for_day(day)
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(_(user_id, 'back'), callback_data='choose_day')],
            [InlineKeyboardButton(_(user_id, 'home'), callback_data='main_menu')],
        ])
        await query.edit_message_text(schedule, parse_mode='Markdown', reply_markup=reply_markup)

    elif query.data == 'main_menu':
        keyboard = [[InlineKeyboardButton(_(user_id, 'view_schedule'), callback_data='choose_day')]]
        await query.edit_message_text(_(user_id, 'main_menu'), reply_markup=InlineKeyboardMarkup(keyboard))

# === ЗАПУСК ===
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("week", week_schedule))
    app.add_handler(CommandHandler("lang", set_language))
    app.add_handler(CommandHandler("add", add_command))
    app.add_handler(CommandHandler("delete", delete_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Бот запущен ✅")
    app.run_polling()
