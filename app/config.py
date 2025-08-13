# Путь к файлу настроек приложения
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "files/settings.json")

# Путь к лог-файлу
LOG_FILE = os.path.join(os.path.dirname(__file__), "files/app_errors.log")