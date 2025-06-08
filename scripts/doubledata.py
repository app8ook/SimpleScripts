from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QSizePolicy, QWidgetItem, QSpacerItem
)
from PyQt5.QtCore import Qt

class DoubledataWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scripts = {
            "filtrdata": {
                "title": "FILTRDATA",
                "process_function": self.filtrdata_data
            },
            "deldata": {
                "title": "DELDATA",
                "process_function": self.deldata_data
            }
        }
        self.current_script = "filtrdata"

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        self.title_label = QLabel(self.scripts[self.current_script]["title"])
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font = self.title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        main_layout.addWidget(self.title_label)

        self.input_label = QLabel("Ввод:")
        main_layout.addWidget(self.input_label)

        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Введите текст")
        main_layout.addWidget(self.input_field)

        self.input_label2 = QLabel("Фильтр:")
        main_layout.addWidget(self.input_label2)

        self.input_field2 = QTextEdit()
        self.input_field2.setPlaceholderText("Введите фильтр")
        self.input_field2.setFixedHeight(80)  # Можно настроить высоту
        main_layout.addWidget(self.input_field2)

        self.output_label = QLabel("Вывод:")
        main_layout.addWidget(self.output_label)

        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        main_layout.addWidget(self.output_field)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        main_layout.addLayout(button_layout)

        self.process_button = QPushButton("Обработать")
        self.process_button.clicked.connect(self.process_text)
        button_layout.addWidget(self.process_button)

        self.back_button = QPushButton("Назад")
        button_layout.addWidget(self.back_button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer)

        self.filtrdata_button = QPushButton("FILTRDATA")
        self.filtrdata_button.clicked.connect(lambda: self.switch_script("filtrdata"))
        button_layout.addWidget(self.filtrdata_button)

        self.deldata_button = QPushButton("DELDATA")
        self.deldata_button.clicked.connect(lambda: self.switch_script("deldata"))
        button_layout.addWidget(self.deldata_button)

        self.update_script_buttons()

    def update_script_buttons(self):
        self.filtrdata_button.setEnabled(self.current_script != "filtrdata")
        self.deldata_button.setEnabled(self.current_script != "deldata")

    def switch_script(self, script_name):
        if script_name not in self.scripts:
            return
        self.current_script = script_name
        self.title_label.setText(self.scripts[script_name]["title"])
        self.update_script_buttons()

        self.output_field.clear()

    def filtrdata_data(self, input_text):
        try:
            input_elements = [element.strip() for line in input_text.split('\n') for element in line.split()]
            filter_elements = [element.strip() for element in self.input_field2.toPlainText().split()]
            filtered_elements = [element for element in input_elements if element in filter_elements]
            filtered_lines = [
                ' '.join(line.split())
                for line in input_text.split('\n')
                if any(element in line for element in filtered_elements)
            ]
            return '\n'.join(filtered_lines)
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def deldata_data(self, input_text):
        try:
            input_elements = [element.strip() for line in input_text.split('\n') for element in line.split()]
            filter_elements = [element.strip() for element in self.input_field2.toPlainText().split()]
            deleted_lines = [
                ' '.join(line.split())
                for line in input_text.split('\n')
                if all(element not in line for element in filter_elements)
            ]
            return '\n'.join(deleted_lines)
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def process_text(self):
        input_text = self.input_field.toPlainText().strip()
        if not input_text:
            self.output_field.setPlainText("Пожалуйста, введите текст для обработки.")
            return
        output_text = self.scripts[self.current_script]["process_function"](input_text)
        self.output_field.setPlainText(output_text)
