from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy

class DuplicatesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        
        self.input_label = QLabel("Ввод:")
        main_layout.addWidget(self.input_label)
        main_layout.setSpacing(10)
        self.input_text = QTextEdit()
        self.input_text.setAcceptRichText(False)
        main_layout.addWidget(self.input_text)

        self.output_label = QLabel("Вывод:")
        main_layout.addWidget(self.output_label)
        main_layout.setSpacing(10)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)

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

    def remove_duplicates_and_count(self, input_text: str) -> str:
        lines = input_text.splitlines()
        unique_lines = list(dict.fromkeys(lines))
        removed_count = len(lines) - len(unique_lines)
        output_text = "\n".join(unique_lines)
        output_text += f"\n\nКоличество уникальных строк: {len(unique_lines)}"
        output_text += f"\nКоличество удаленных дубликатов: {removed_count}"
        return output_text

    def process_text(self):
        input_data = self.input_text.toPlainText()
        result = self.remove_duplicates_and_count(input_data)
        self.output_text.setPlainText(result)
