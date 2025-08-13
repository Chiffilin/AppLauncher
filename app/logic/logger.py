import sys
import traceback
from datetime import datetime

from app.config import LOG_FILE


def log_message(message):
    """Пишет любое сообщение в лог."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")

def log_exception(e):
    """Пишет исключение с трассировкой в лог."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "="*80 + "\n")
        f.write(f"Время: {datetime.now()}\n")
        f.write(f"Ошибка: {repr(e)}\n")
        f.write("Трассировка:\n")
        f.write("".join(traceback.format_exc()))
        f.write("="*80 + "\n")

# Назначаем глобальный обработчик исключений
sys.excepthook = log_exception