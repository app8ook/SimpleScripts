from itertools import product
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit, 
    QPushButton, QSizePolicy, QSpacerItem
)

class GeneratorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        
        self.title_label = QLabel("Генератор номеров по шаблону")
        font = self.title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        main_layout.addWidget(self.title_label)

        self.input_label = QLabel("Введите шаблон (например, 7971627843XXX):")
        main_layout.addWidget(self.input_label)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Используйте только цифры и заглавную X")
        main_layout.addWidget(self.input_field)

        self.output_label = QLabel("Вывод:")
        main_layout.addWidget(self.output_label)
        
        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        main_layout.addWidget(self.output_field)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        main_layout.addLayout(button_layout)
        
        self.process_button = QPushButton("Сгенерировать")
        self.process_button.clicked.connect(self.process_text)
        button_layout.addWidget(self.process_button)

        self.back_button = QPushButton("Назад")
        button_layout.addWidget(self.back_button)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer)

    def process_text(self):
        template = self.input_field.text().strip().upper()
        
        if not template:
            self.output_field.setPlainText("Шаблон не может быть пустым.")
            return
            
        if any(char not in "0123456789X" for char in template):
            self.output_field.setPlainText("Используйте только цифры и символ X.")
            return

        x_count = template.count("X")
        if x_count > 6:
            self.output_field.setPlainText("Слишком много X (больше 6). Программа может зависнуть при отрисовке!")
            return
            
        if x_count == 0:
            self.output_field.setPlainText(f"{template}\n\nНет символов X для замены.")
            return

        results = []
        # Генерация комбинаций
        for combination in product("0123456789", repeat=x_count):
            number = template
            for digit in combination:
                number = number.replace("X", digit, 1)
            results.append(number)

        output_text = "\n".join(results)
        output_text += f"\n\nСоздано комбинаций: {len(results)}"
        self.output_field.setPlainText(output_text)