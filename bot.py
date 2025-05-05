from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, ConversationHandler, filters

# ID администратора, куда будут отправляться ответы
ADMIN_CHAT_ID = 493385247

# Этапы диалога
Q1, Q2, Q3, Q4 = range(4)

user_answers = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_answers[user_id] = {}

    await update.message.reply_text(
        "🙏 Спасибо за доверие к нашей станции!\n"
        "Мы хотим стать ещё лучше, и нам важно Ваше мнение.\n\n"
        "1️⃣ Откуда вы о нас узнали?",
        reply_markup=ReplyKeyboardMarkup(
            [["Instagram", "Facebook"], ["Dobry mechanik", "Друг посоветовал"], ["Google", "Другое"]],
            one_time_keyboard=True, resize_keyboard=True
        )
    )
    return Q1

async def answer_q1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_answers[user_id]["Источник"] = update.message.text

    await update.message.reply_text(
        "2️⃣ Как бы Вы оценили наше обслуживание от 1 до 10?",
        reply_markup=ReplyKeyboardMarkup(
            [[str(i) for i in range(1, 11)]],
            one_time_keyboard=True, resize_keyboard=True
        )
    )
    return Q2

async def answer_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_answers[user_id]["Оценка"] = update.message.text

    await update.message.reply_text(
        "3️⃣ Хотели бы Вы первым получать информацию о наших акциях?",
        reply_markup=ReplyKeyboardMarkup(
            [["Да", "Нет"]],
            one_time_keyboard=True, resize_keyboard=True
        )
    )
    return Q3

async def answer_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_answers[user_id]["Получать акции"] = update.message.text

    await update.message.reply_text("4️⃣ Напишите, пожалуйста, Ваши пожелания или предложения для нашего СТО:")
    return Q4

async def answer_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_answers[user_id]["Пожелания"] = update.message.text

    data = user_answers[user_id]
    text = (
        f"📩 Новый отзыв:\n\n"
        f"Источник: {data['Источник']}\n"
        f"Оценка: {data['Оценка']}/10\n"
        f"Получать акции: {data['Получать акции']}\n"
        f"Пожелания: {data['Пожелания']}"
    )

    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await update.message.reply_text("✅ Спасибо за ответы! Мы ценим Ваше мнение. Хорошего дня!")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Опрос отменён. Если захотите пройти снова — нажмите /start.")
    return ConversationHandler.END

# Инициализация
app = ApplicationBuilder().token("8098703773:AAEXa_lfk7_8GVjWH8Roy1rz_veFNBDUqFc").build()

# Обработка диалога
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_q1)],
        Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_q2)],
        Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_q3)],
        Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_q4)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)

# Запуск
app.run_polling()
