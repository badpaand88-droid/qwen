import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dashscope import Generation
import dashscope
import os

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем ключи из переменных окружения
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

dashscope.api_key = DASHSCOPE_API_KEY

# Хранилище для истории (в реальном приложении используйте БД)
user_histories = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_message = update.message.text
    
    # Инициализация истории для пользователя
    if user_id not in user_histories:
        user_histories[user_id] = []
    
    # Добавляем сообщение пользователя
    user_histories[user_id].append({"role": "user", "content": user_message})
    
    # Ограничиваем историю (опционально)
    if len(user_histories[user_id]) > 10:
        user_histories[user_id] = user_histories[user_id][-10:]
    
    try:
        # Вызов Qwen
        response = Generation.call(
            model='qwen-turbo',
            messages=user_histories[user_id],
            result_format='message'
        )
        ai_text = response.output.choices[0].message.content
        
        # Добавляем ответ в историю
        user_histories[user_id].append({"role": "assistant", "content": ai_text})
        
    except Exception as e:
        ai_text = "Извините, произошла ошибка при обработке запроса."
        logging.error(f"Ошибка вызова Qwen: {e}")
    
    await update.message.reply_text(ai_text)

def run_bot():
    """Функция для запуска бота"""
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app

if __name__ == '__main__':
    app = run_bot()
    app.run_polling()
