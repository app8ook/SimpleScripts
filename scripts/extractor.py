import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt

class ExtractorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.scripts = {
            "email": {
                "title": "Экстрактор (Email)",
                "process_function": self.extract_emails
            },
            "url": {
                "title": "Экстрактор (URL)",
                "process_function": self.extract_urls
            }
        }
        self.current_script = "email"
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        
        self.title_label = QLabel(self.scripts[self.current_script]["title"])
        font = self.title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        main_layout.addWidget(self.title_label)

        self.input_label = QLabel("Ввод любого текста:")
        main_layout.addWidget(self.input_label)
        
        self.input_field = QTextEdit()
        self.input_field.setAcceptRichText(False)
        self.input_field.setPlaceholderText("Вставьте сюда массив текста, исходный код или любой мусор...")
        main_layout.addWidget(self.input_field)

        self.output_label = QLabel("Найденные данные (без дубликатов):")
        main_layout.addWidget(self.output_label)
        
        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        main_layout.addWidget(self.output_field)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        main_layout.addLayout(button_layout)
        
        self.process_button = QPushButton("Извлечь")
        self.process_button.clicked.connect(self.process_text)
        button_layout.addWidget(self.process_button)

        self.back_button = QPushButton("Назад")
        button_layout.addWidget(self.back_button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer)

        self.email_button = QPushButton("Режим EMAIL")
        self.email_button.clicked.connect(lambda: self.switch_script("email"))
        button_layout.addWidget(self.email_button)

        self.url_button = QPushButton("Режим URL")
        self.url_button.clicked.connect(lambda: self.switch_script("url"))
        button_layout.addWidget(self.url_button)

        self.update_script_buttons()

    def update_script_buttons(self):
        self.email_button.setEnabled(self.current_script != "email")
        self.url_button.setEnabled(self.current_script != "url")

    def switch_script(self, script_name):
        if script_name not in self.scripts:
            return
        self.current_script = script_name
        self.title_label.setText(self.scripts[script_name]["title"])
        self.update_script_buttons()
        self.output_field.clear()

    def extract_emails(self, text):
        pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        matches = re.findall(pattern, text)
        # Удаляем дубликаты с сохранением порядка
        unique_matches = list(dict.fromkeys(matches)) 
        
        output_text = "\n".join(unique_matches)
        output_text += f"\n\nНайдено уникальных Email: {len(unique_matches)}"
        return output_text

    def extract_urls(self, text):
        # Поиск http/https, а также ссылок начинающихся с www.
        pattern = r'https?://[^\s<>"\']+|(?:www\.)[^\s<>"\']+'
        matches = re.findall(pattern, text)
        unique_matches = list(dict.fromkeys(matches))
        
        output_text = "\n".join(unique_matches)
        output_text += f"\n\nНайдено уникальных URL: {len(unique_matches)}"
        return output_text

    def process_text(self):
        input_text = self.input_field.toPlainText()
        if not input_text.strip():
            self.output_field.setPlainText("Пожалуйста, введите текст для поиска.")
            return
            
        output_text = self.scripts[self.current_script]["process_function"](input_text)
        self.output_field.setPlainText(output_text)