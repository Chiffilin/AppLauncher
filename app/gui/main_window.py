import os
import sys

from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow

from app.gui.ui_main_window import Ui_MainWindow
from app.logic.work_with_json import load_settings_from_json, save_settings_to_json
from app.logic.work_with_pywin32 import add_app_to_task_scheduler, remove_app_from_task_scheduler


# Логика получения пути к файлу
def get_executable_path() -> str:
    """Открывает диалог для выбора исполняемого файла."""
    file_path, _ = QFileDialog.getOpenFileName(
        None, "Виберіть програму для автозапуску", "", "Програми (*.exe)"
    )
    return file_path



class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Модель данных для QListView
        self.model = QStringListModel()
        self.ui.listView.setModel(self.model)

        # Загружаем все настройки при запуске
        settings = load_settings_from_json()
        self._app_paths = settings.get("app_paths", {})
        self.autostart_enabled = settings.get("autostart_enabled", False)

        # Устанавливаем флажок в сохранённое положение
        self.ui.autostartCheckBox.setChecked(self.autostart_enabled)


        # Загружаем список при запуске приложения
        self.model.setStringList(list(self._app_paths.keys()))
        print(f"Текущий список программ: {self.model.stringList()}")

        # Подключаем кнопку "Добавить"
        self.ui.addButton.clicked.connect(self.on_add_button_clicked)

        # Подключаем кнопку "Удалить"
        self.ui.deleteButton.clicked.connect(self.on_delete_button_clicked)

        # Подключаем кнопку "Автозапуск"
        self.ui.autostartCheckBox.toggled.connect(self.on_autostart_toggled)

    def on_add_button_clicked(self) -> None:
        """Обработка нажатия кнопки 'Додати'."""
        print("Нажата кнопка 'Додати'!")
        app_path = get_executable_path()
        if app_path:
            self.add_new_app(app_path)


    def on_delete_button_clicked(self) -> None:
        """Удаляет выбранный элемент из списка и обновляет модель."""
        print("Нажата кнопка 'Удалить'")
        selected_indexes = self.ui.listView.selectedIndexes()

        if not selected_indexes:
            return

        index = selected_indexes[0]
        file_name_to_remove = self.model.data(index)

        # Удаляем из словаря и обновляем модель
        if file_name_to_remove in self._app_paths:
            del self._app_paths[file_name_to_remove]
            self.model.setStringList(list(self._app_paths.keys()))

    def on_autostart_toggled(self, checked: bool)->None:
        """
        Метод, который вызывается при изменении состояния флажка.
        :param checked: True, если флажок установлен, False — если снят.
        """
        self.autostart_enabled = checked

        if checked:
            print("Флажок 'Автозапуск' установлен.")
            # self.update_autostart_registry()
            self.add_all_app_to_task()
        else:
            print("Флажок 'Автозапуск' снят.")
            # self.clear_autostart_registry()
            self.delete_all_app_from_task()

    def closeEvent(self, event) -> None:
        """Сохраняем все настройки при закрытии окна."""
        settings_to_save = {
            "app_paths": self._app_paths,
            "autostart_enabled": self.autostart_enabled
        }
        save_settings_to_json(settings_to_save)
        event.accept()

    def add_new_app(self, full_path: str) -> None:
        """Добавляет новый путь в словарь, если его там нет, и обновляет отображение."""
        file_name = os.path.basename(full_path)

        if file_name not in self._app_paths:
            self._app_paths[file_name] = full_path
            self.model.setStringList(list(self._app_paths.keys()))
        else:
            print("Эта программа уже есть в списке.")

    def add_all_app_to_task(self) -> None:
        """Добавление все приложения в список задач."""

        # Перебираем наш словарь с приложениями и добавляем каждое в реестр
        for app_name, app_path in self._app_paths.items():
            add_app_to_task_scheduler(app_name,app_path)

    def delete_all_app_from_task(self) -> None:
        """Удаляем все приложения из списка задач."""

        # Перебираем наш словарь с приложениями и добавляем каждое в реестр
        for app_name, app_path in self._app_paths.items():
            remove_app_from_task_scheduler(app_name)


def app_start():
    print("Приложение запущено. Начало выполнения.")
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    app_start()