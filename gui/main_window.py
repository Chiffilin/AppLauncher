import os
import sys
import json

from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFileDialog, QMainWindow

from gui.ui_main_window import Ui_MainWindow

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

        # Словарь для хранения полного пути (ключ - имя файла, значение - полный путь)
        self._app_paths: dict[str, str] = {}

        # Загружаем список при запуске приложения
        self._app_paths = self.load_apps_from_json()
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
        if checked:
            print("Флажок 'Автозапуск' установлен.")
            # Здесь можно добавить логику для добавления в автозапуск
        else:
            print("Флажок 'Автозапуск' снят.")
            # Здесь можно добавить логику для удаления из автозапуска




    def closeEvent(self, event) -> None:
        """Сохраняем список при закрытии окна."""
        self.save_apps_to_json(self._app_paths)
        event.accept()

    def add_new_app(self, full_path: str) -> None:
        """Добавляет новый путь в словарь, если его там нет, и обновляет отображение."""
        file_name = os.path.basename(full_path)

        if file_name not in self._app_paths:
            self._app_paths[file_name] = full_path
            self.model.setStringList(list(self._app_paths.keys()))
        else:
            print("Эта программа уже есть в списке.")

    def save_apps_to_json(self, apps_dict: dict[str, str]) -> None:
        """Сохраняет словарь путей к программам в JSON-файл."""
        try:
            with open("autostart_config.json", "w", encoding='utf-8') as file_config:
                json.dump(apps_dict, file_config, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    def load_apps_from_json(self) -> dict[str, str]:
        """
        Загружает словарь путей к программам из JSON-файла.
        Обрабатывает старые форматы, основанные на списках.
        """
        try:
            with open("autostart_config.json", "r", encoding='utf-8') as file_config:
                data = json.load(file_config)
                # Проверяем, является ли загруженный файл старым форматом
                if isinstance(data, list):
                    print("Загружен старый формат файла. Конвертируем в новый формат.")
                    new_data = {}
                    for full_path in data:
                        file_name = os.path.basename(full_path)
                        new_data[file_name] = full_path

                    return new_data

                # Если это уже словарь, возвращаем его как есть
                elif isinstance(data, dict):
                    return data

                # Для любого другого неожиданного формата
                else:
                    print("Неизвестный формат файла. Создан пустой словарь.")
                    return {}

        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл настроек не найден или поврежден. Создан пустой словарь.")
            return {}

def app_start():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    app_start()