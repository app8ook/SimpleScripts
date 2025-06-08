from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QSizePolicy, QSpacerItem, QPlainTextEdit, QApplication
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeySequence

class NumWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scripts = {
            "numbd": {
                "title": "NUMBD",
                "process_function": self.process_data_numbd
            },
            "numadmn": {
                "title": "NUMADMN",
                "process_function": self.process_data_numadmn
            }
        }
        self.current_script = "numbd"

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # Заголовок
        self.title_label = QLabel(self.scripts[self.current_script]["title"])
        font = self.title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        main_layout.addWidget(self.title_label)

        # Метка "Ввод:"
        self.input_label = QLabel("Ввод:")
        main_layout.addWidget(self.input_label)

        # Поле ввода
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Введите текст")
        main_layout.addWidget(self.input_field)

        # Метка "Вывод:"
        self.output_label = QLabel("Вывод:")
        main_layout.addWidget(self.output_label)

        # Поле вывода (только для чтения)
        self.output_field = QPlainTextEdit()
        self.output_field.setReadOnly(True)
        main_layout.addWidget(self.output_field)
        
        # Устанавливаем фильтр событий на output_field
        self.output_field.installEventFilter(self)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
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

        self.numbd_button = QPushButton("NUMBD")
        self.numbd_button.clicked.connect(lambda: self.switch_script("numbd"))
        button_layout.addWidget(self.numbd_button)

        self.numadmn_button = QPushButton("NUMADMN")
        self.numadmn_button.clicked.connect(lambda: self.switch_script("numadmn"))
        button_layout.addWidget(self.numadmn_button)

        self.update_script_buttons()

    def eventFilter(self, obj, event):  # Перехватываем Ctrl+C для нормальной обработки
        if obj == self.output_field and event.type() == QEvent.KeyPress:
            if event.matches(QKeySequence.Copy):
                self.copy_plain_text()
                return True
        return super().eventFilter(obj, event)

    def copy_plain_text(self):
        text = self.output_field.toPlainText()
        QApplication.clipboard().setText(text)

    def update_script_buttons(self):
        self.numbd_button.setEnabled(self.current_script != "numbd")
        self.numadmn_button.setEnabled(self.current_script != "numadmn")

    def switch_script(self, script_name):
        if script_name not in self.scripts:
            return
        self.current_script = script_name
        script_info = self.scripts[script_name]
        self.title_label.setText(script_info["title"])
        self.update_script_buttons()
        self.output_field.clear()

    def process_data_numbd(self, input_text):
        lines = input_text.splitlines()
        header = "Дата\tЦена\tНомер\tОписание"
        output_lines = [header]
        for i, line in enumerate(lines, start=1):
            try:
                if "Balance refill" in line or "Phone number verification" in line:
                    output_lines.append(line)
                    continue
                parts = line.split(",")
                if len(parts) < 5:
                    raise ValueError(f"В строке {i} недостаточно данных.")
                date = parts[0].strip('"')
                price = parts[2].replace("-", "").replace(".", ",")
                if "Monthly charge for renting a phone number" in parts[4]:
                    number = parts[4].split("'")[1]
                    description = "Абонентская плата"
                elif "Connection cost for a phone number" in parts[4]:
                    number = parts[4].split("'")[1]
                    description = "Плата за подключение"
                else:
                    number = parts[4].split("'")[1] if "'" in parts[4] else ""
                    description = parts[4].replace("'", "")
                output_line = f"{date}\t{price}\t{number}\t{description}"
                output_lines.append(output_line)
            except Exception as e:
                output_lines.append(f"Ошибка: {str(e)}")
        output_text = "\n".join(output_lines)
        return output_text

    def process_data_numadmn(self, input_text):
        lines = input_text.splitlines()
        header = "Дата\tЦена\tНомер\tОписание"
        output_lines = [header]
        for i, line in enumerate(lines, start=1):
            try:
                if "Пополнение" in line or "Верификация" in line or "тикет" in line or "Счет" in line:
                    output_lines.append(line)
                    continue
                parts = line.split("\t")
                if len(parts) < 3:
                    raise ValueError(f"В строке {i} недостаточно данных.")
                date = parts[0].replace(",", ".")
                price = parts[1].replace("-", "").replace(".", ",")
                if "Ежемесячное списание за использование номера" in parts[2]:
                    number = parts[2].split(" ")[-1]
                    description = "Абонентская плата"
                elif "A number margin: Списание за А-номер:" in parts[2]:
                    number = parts[2].split(": ")[-1]
                    description = "Абонентская плата"
                    price = parts[3].replace("-", "").replace(".", ",")
                elif "Payment for A number" in parts[2]:
                    number = parts[2].split(" ")[-1]
                    description = "Плата за подключение"
                    price = parts[3].replace("-", "").replace(".", ",")
                elif "Списание за подключение номера" in parts[2]:
                    number = parts[2].split(" ")[-1]
                    description = "Плата за подключение"
                    price = parts[1].replace("-", "").replace(".", ",")
                elif "HLR" in parts[2]:
                    number = ""
                    description = "HLR"
                    price = parts[1].replace("-", "").replace(".", ",")
                else:
                    number = parts[2]
                    description = parts[2]
                output_line = f"{date}\t{price}\t{number}\t{description}"
                output_lines.append(output_line)
            except Exception as e:
                output_lines.append(f"Ошибка: {str(e)}")
        output_text = "\n".join(output_lines)
        return output_text

    def process_text(self):
        input_text = self.input_field.toPlainText().strip()
        if not input_text:
            self.output_field.setPlainText("Пожалуйста, введите текст для обработки.")
            return
        output_text = self.scripts[self.current_script]["process_function"](input_text)
        self.output_field.setPlainText(output_text)
