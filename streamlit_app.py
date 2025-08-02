import streamlit as st
import subprocess
import os
from dotenv import load_dotenv

# Загружаем локальные переменные окружения (для тестирования)
if os.path.exists('.env'):
    load_dotenv()

st.set_page_config(page_title="Telegram Qwen Bot Manager", page_icon="🤖")

st.title("🤖 Управление Telegram-ботом Qwen")

# Секреты из Streamlit Cloud
DASHSCOPE_API_KEY = st.secrets.get("DASHSCOPE_API_KEY")
TELEGRAM_BOT_TOKEN = st.secrets.get("TELEGRAM_BOT_TOKEN")

if not DASHSCOPE_API_KEY or not TELEGRAM_BOT_TOKEN:
    st.error("⚠️ Пожалуйста, добавьте DASHSCOPE_API_KEY и TELEGRAM_BOT_TOKEN в secrets.toml")
    st.stop()

# Сохраняем секреты в переменные окружения
os.environ['DASHSCOPE_API_KEY'] = DASHSCOPE_API_KEY
os.environ['TELEGRAM_BOT_TOKEN'] = TELEGRAM_BOT_TOKEN

# Состояние бота
if 'bot_process' not in st.session_state:
    st.session_state.bot_process = None

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Запустить бота", use_container_width=True):
        if st.session_state.bot_process is None:
            try:
                st.session_state.bot_process = subprocess.Popen(['python', 'bot.py'])
                st.success("✅ Бот запущен!")
            except Exception as e:
                st.error(f"❌ Ошибка запуска: {e}")
        else:
            st.warning("⚠️ Бот уже запущен")

with col2:
    if st.button("🛑 Остановить бота", use_container_width=True):
        if st.session_state.bot_process:
            st.session_state.bot_process.terminate()
            st.session_state.bot_process = None
            st.success("✅ Бот остановлен")
        else:
            st.warning("⚠️ Бот не запущен")

st.divider()

# Информация
st.subheader("ℹ️ Инструкция")
st.markdown("""
1. Убедитесь, что вы добавили секреты в Streamlit Cloud
2. Нажмите "Запустить бота"
3. Найдите своего бота в Telegram и начните чат
4. Для остановки используйте кнопку "Остановить бота"
""")

# Логи (опционально)
if st.checkbox("📝 Показать логи"):
    st.info("Логи доступны в консоли Streamlit Cloud")
