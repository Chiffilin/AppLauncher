from PySide6.QtWidgets import QFileDialog, QApplication

def get_executable_path()-> str:
    # app = QApplication([])
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(
        None, "Выберите программу для автозапуска", "", "Программы (*.exe)"
    )
    return file_path



def main():
    # Пример использования
    app_path = get_executable_path()
    if app_path:
        print(f"Выбрана программа: {app_path}")


if __name__ == "__main__":
    main()
