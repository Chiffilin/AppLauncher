import sys
import json
from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFileDialog, QMainWindow

from gui.ui_main_window import Ui_MainWindow

# Логика получения пути к файлу
def get_executable_path() -> str:
    # Здесь можно использовать QFileDialog из вашего основного приложения
    # Например:
    file_path, _ = QFileDialog.getOpenFileName(
        None, "Виберіть програму для автозапуску", "", "Програми (*.exe)"
    )
    return file_path

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = QStringListModel()
        self.ui.listView.setModel(self.model)

        # Загружаем список при запуске приложения
        file_paths = self.load_apps_from_json()
        self.model.setStringList(file_paths)
        print(f"Текущий список программ: {self.model.stringList()}")

        # Подключаем кнопку "Добавить"
        self.ui.addButton.clicked.connect(self.on_add_button_clicked)

        # Подключаем кнопку "Удалить"
        self.ui.deleteButton.clicked.connect(self.on_delete_button_clicked)

    def on_add_button_clicked(self) -> None:
        """Обработка нажатия кнопки 'Додати'."""
        print("Нажата кнопка 'Додати'!")
        app_path = get_executable_path()
        if app_path:
            self.add_new_app(app_path)


    def on_delete_button_clicked(self) -> None:
        """Удаляет выбранный элемент из списка и обновляет файл."""
        # Получаем выбранный индекс
        print("Нажата кнопка удалить")
        # Если ни один элемент не выбран, ничего не делаем
        selected_indexes = self.ui.listView.selectedIndexes()
        if not selected_indexes:
            return

        # Получаем первый выбранный индекс
        index = selected_indexes[0]

        # Удаляем строку из модели
        self.model.removeRow(index.row())

        # Обновляем JSON-файл, чтобы отразить изменение
        self.save_apps_to_json(self.model.stringList())

    def closeEvent(self, event) -> None:
        """Сохраняем список при закрытии окна."""
        self.save_apps_to_json(self.model.stringList())
        event.accept()

    def add_new_app(self, new_app_path: str) -> None:
        """Добавляет новый путь в модель, если его там нет."""
        current_apps = self.model.stringList()
        if new_app_path not in current_apps:
            current_apps.append(new_app_path)
            self.model.setStringList(current_apps)

    def save_apps_to_json(self, apps_list: list) -> None:
        """Сохраняет список путей к программам в JSON-файл."""
        try:
            with open("autostart_config.json", "w", encoding='utf-8') as file_config:
                json.dump(apps_list, file_config, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    def load_apps_from_json(self) -> list:
        """Загружает список путей к программам из JSON-файла."""
        try:
            with open("autostart_config.json", "r", encoding='utf-8') as file_config:
                return json.load(file_config)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл настроек не найден или поврежден. Создан пустой список.")
            return []

def app_start():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    app_start()