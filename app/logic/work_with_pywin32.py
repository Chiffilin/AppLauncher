import win32com.client
import traceback
from datetime import datetime

from app.config import LOG_FILE


def log_exception(e):
    """Пишет исключение с трассировкой в лог."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "="*80 + "\n")
        f.write(f"Время: {datetime.now()}\n")
        f.write(f"Ошибка: {repr(e)}\n")
        f.write("Трассировка:\n")
        f.write("".join(traceback.format_exc()))
        f.write("="*80 + "\n")


def add_app_to_task_scheduler(app_name, app_path):
    try:
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()

        root_folder = scheduler.GetFolder("\\")

        # Создаем новую задачу
        task_def = scheduler.NewTask(0)

        # Триггер — запуск при входе пользователя
        trigger = task_def.Triggers.Create(9)  # TASK_TRIGGER_LOGON
        trigger.Id = "LogonTrigger"
        trigger.UserId = ""  # Пусто = текущий пользователь

        # Действие — запуск программы
        action = task_def.Actions.Create(0)  # TASK_ACTION_EXEC
        action.Path = app_path

        # Параметры безопасности — запуск от имени текущего пользователя
        task_def.Principal.UserId = ""  # "" или getpass.getuser()
        task_def.Principal.LogonType = 3  # TASK_LOGON_INTERACTIVE_TOKEN
        task_def.Principal.RunLevel = 1   # TASK_RUNLEVEL_LUA

        # Регистрация задачи
        root_folder.RegisterTaskDefinition(
            app_name,
            task_def,
            6,           # TASK_CREATE_OR_UPDATE
            None,  # текущий пользователь
            None,  # пароль
            3            # TASK_LOGON_PASSWORD
        )

        print(f"✅ Задача '{app_name}' добавлена.")
    except Exception as e:
        print(f"❌ Ошибка при добавлении задачи: {e}")
        log_exception(e)


def remove_app_from_task_scheduler(app_name):
    try:
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()

        root_folder = scheduler.GetFolder("\\")
        root_folder.DeleteTask(app_name, 0)

        print(f"✅ Задача '{app_name}' удалена.")
    except Exception as e:
        print(f"❌ Ошибка при удалении задачи: {e}")
        log_exception(e)


if __name__ == "__main__":
    # Пример
    EXE_PATH = r"C:\Windows\System32\notepad.exe"
    TASK_NAME = "TestAutoStart"

    # Добавить задачу
    add_task(TASK_NAME, EXE_PATH)

    # Удалить задачу
    # remove_task(TASK_NAME)
