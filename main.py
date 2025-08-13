import sys

from app.gui.main_window import app_start
from app.logic.logger import log_exception


def main():
    app_start()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Перехват любых ошибок при старте
        log_exception(*sys.exc_info())
