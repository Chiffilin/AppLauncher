import json

from app.config import SETTINGS_FILE


def save_settings_to_json(settings_data: dict) -> None:
    """Сохраняет все настройки в JSON-файл."""
    try:
        with open(SETTINGS_FILE, "w", encoding='utf-8') as file_config:
            json.dump(settings_data, file_config, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")




def load_settings_from_json() -> dict:
    """Загружает все настройки из JSON-файла."""
    try:
        with open(SETTINGS_FILE, "r", encoding='utf-8') as file_config:
            return json.load(file_config)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Файл настроек не найден или поврежден. Созданы настройки по умолчанию.")
        # Возвращаем настройки по умолчанию, если файл не найден
        return {"app_paths": {}, "autostart_enabled": False}
