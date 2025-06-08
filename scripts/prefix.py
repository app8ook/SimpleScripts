from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt

class PrefixWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scripts = {
            "prefiltr": {
                "title": "PREFILTR",
                "process_function": self.prefiltr
            },
            "prefdel": {
                "title": "PREFDEL",
                "process_function": self.prefdel
            }
        }
        self.current_script = "prefiltr"

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

        self.prefix_label = QLabel("Префикс:")
        main_layout.addWidget(self.prefix_label)

        self.prefix_field = QTextEdit()
        self.prefix_field.setFixedHeight(40)
        self.prefix_field.setPlaceholderText("Введите префикс")
        main_layout.addWidget(self.prefix_field)

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

        self.prefiltr_button = QPushButton("PREFILTR")
        self.prefiltr_button.clicked.connect(lambda: self.switch_script("prefiltr"))
        button_layout.addWidget(self.prefiltr_button)

        self.prefdel_button = QPushButton("PREFDEL")
        self.prefdel_button.clicked.connect(lambda: self.switch_script("prefdel"))
        button_layout.addWidget(self.prefdel_button)

        self.update_script_buttons()

    def update_script_buttons(self):
        self.prefiltr_button.setEnabled(self.current_script != "prefiltr")
        self.prefdel_button.setEnabled(self.current_script != "prefdel")

    def switch_script(self, script_name):
        if script_name not in self.scripts:
            return
        self.current_script = script_name
        self.title_label.setText(self.scripts[script_name]["title"])
        self.update_script_buttons()
        self.output_field.clear()

    def prefiltr(self, input_text, prefix):
        lines = [line for line in input_text.splitlines() if line.strip()]
        original_count = len(lines)
        filtered_lines = [line for line in lines if line.startswith(prefix)]
        filtered_count = len(filtered_lines)
        removed_count = original_count - filtered_count
        output_text = "\n".join(filtered_lines)
        output_text += f"\n\nКоличество не попавших под фильтр строк: {removed_count}"
        output_text += f"\nКоличество отфильтрованных строк с указанным префиксом: {filtered_count}"
        return output_text

    def prefdel(self, input_text, prefix):
        lines = input_text.splitlines()
        original_count = len(lines)
        filtered_lines = [line for line in lines if not line.startswith(prefix)]
        removed_count = original_count - len(filtered_lines)
        output_text = "\n".join(filtered_lines)
        output_text += f"\n\nКоличество оставшихся строк: {len(filtered_lines)}"
        output_text += f"\nКоличество удаленных строк с указанным префиксом: {removed_count}"
        return output_text

    def process_text(self):
        input_text = self.input_field.toPlainText().strip()
        prefix = self.prefix_field.toPlainText()
        if not input_text:
            self.output_field.setPlainText("Пожалуйста, введите текст для обработки.")
            return
        if prefix == "":
            self.output_field.setPlainText("Пожалуйста, введите префикс.")
            return
        output_text = self.scripts[self.current_script]["process_function"](input_text, prefix)
        self.output_field.setPlainText(output_text)
