import os
import sys
import winreg

def add_to_autostart():
    """Добавляет текущее приложение в реестр автозапуска Windows."""
    # Получаем полный путь к исполняемому файлу нашего приложения
    app_path = sys.executable
    app_name = os.path.basename(app_path)

    # Ключ реестра для автозапуска
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        # Открываем ключ реестра
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)

        # Добавляем наше приложение в реестр
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{app_path}"')
        winreg.CloseKey(key)
        print(f"Приложение '{app_name}' успешно добавлено в автозапуск.")
        return True
    except Exception as e:
        print(f"Ошибка при добавлении в автозапуск: {e}")
        return False

def remove_from_autostart():
    """Удаляет текущее приложение из реестра автозапуска Windows."""
    app_name = os.path.basename(sys.executable)
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, app_name)
        winreg.CloseKey(key)
        print(f"Приложение '{app_name}' успешно удалено из автозапуска.")
    except FileNotFoundError:
        print(f"Приложение '{app_name}' не найдено в реестре автозапуска.")
    except Exception as e:
        print(f"Ошибка при удалении из автозапуска: {e}")