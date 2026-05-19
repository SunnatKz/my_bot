import os
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("Ошибка: токен не найден!")
    exit(1)

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Привет! Напиши свою цель, я напомню через 24 часа.")

async def save_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    goal_text = update.message.text
    remind_time = datetime.now() + timedelta(hours=24)
    
    user_data[user_id] = {"goal": goal_text, "time": remind_time}
    
    await update.message.reply_text(f"✅ Запомнил: {goal_text}\nНапомню через 24 часа.")
    
    context.job_queue.run_once(
        remind_user,
        when=24*60*60,
        data={"user_id": user_id, "goal": goal_text}
    )

async def remind_user(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data
    await context.bot.send_message(
        chat_id=data["user_id"],
        text=f"⏰ НАПОМИНАНИЕ!\nТы хотел: {data['goal']}\n\nСделал?"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_goal))
    
    print("✅ Бот запущен на Render!")
    app.run_polling()

if __name__ == "__main__":
    main()
