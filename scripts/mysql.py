from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt

class MysqlWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.scripts = {
            "ivr": {
                "title": "IVR",
                "context_label": "Контекст:",
                "context_hint": "Введите контекст",
                "client_label": "Клиент:",
                "client_hint": "Введите ID",
                "prefix_label": "",
                "prefix_hint": "",
                "main_label": "Путь к IVR:",
                "ivr_hint": "Введите путь к IVR"
            },
            "ivr_to_inc": {
                "title": "IVRTOINC",
                "context_label": "Контекст:",
                "context_hint": "Введите контекст",
                "client_label": "Клиент:",
                "client_hint": "Введите ID",
                "prefix_label": "Префикс:",
                "prefix_hint": "Введите префикс",
                "main_label": "",
                "ivr_hint": ""
            },
            "ivr_lv": {
                "title": "IVRLV",
                "context_label": "Контекст:",
                "context_hint": "Введите контекст",
                "client_label": "Клиент:",
                "client_hint": "Введите ID",
                "prefix_label": "",
                "prefix_hint": "",
                "main_label": "",
                "ivr_hint": ""
            },
            "inc": {
                "title": "INC",
                "context_label": "Контекст:",
                "context_hint": "Введите контекст",
                "client_label": "Клиент:",
                "client_hint": "Введите ID",
                "prefix_label": "Префикс:",
                "prefix_hint": "Введите префикс",
                "main_label": "",
                "ivr_hint": ""
            },
            "inc_to_ivr": {
                "title": "INCTOIVR",
                "context_label": "Контекст:",
                "context_hint": "Введите контекст",
                "client_label": "Клиент:",
                "client_hint": "Введите ID",
                "prefix_label": "",
                "prefix_hint": "",
                "main_label": "Путь к IVR:",
                "ivr_hint": "Введите путь к IVR"
            },
            "del": {
                "title": "DEL",
                "context_label": "",
                "context_hint": "",
                "client_label": "",
                "client_hint": "",
                "prefix_label": "",
                "prefix_hint": "",
                "main_label": "",
                "ivr_hint": ""
            }
        }

        self.current_script = "ivr"
        self.init_ui()
        self.switch_script(self.current_script)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        self.title_label = QLabel()
        font = self.title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        main_layout.addWidget(self.title_label)

        self.numbers_label = QLabel("Номера:")
        main_layout.addWidget(self.numbers_label)

        self.numbers_field = QTextEdit()
        self.numbers_field.setPlaceholderText("Введите номера через новую строку")
        main_layout.addWidget(self.numbers_field)

        self.context_label = QLabel()
        main_layout.addWidget(self.context_label)

        self.context_field = QLineEdit()
        main_layout.addWidget(self.context_field)

        self.client_label = QLabel()
        main_layout.addWidget(self.client_label)

        self.client_field = QLineEdit()
        main_layout.addWidget(self.client_field)

        self.main_label = QLabel()
        main_layout.addWidget(self.main_label)

        self.main_field = QLineEdit()
        main_layout.addWidget(self.main_field)

        self.prefix_label = QLabel()
        main_layout.addWidget(self.prefix_label)

        self.prefix_field = QLineEdit()
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

        self.generate_button = QPushButton("Сгенерировать")
        self.generate_button.clicked.connect(self.generate_query)
        button_layout.addWidget(self.generate_button)

        self.back_button = QPushButton("Назад")
        button_layout.addWidget(self.back_button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer)

        self.buttons = {} # Кнопки переключения скриптов
        for key in ["ivr", "ivr_to_inc", "ivr_lv", "inc", "inc_to_ivr", "del"]:
            btn = QPushButton(self.scripts[key]["title"])
            btn.clicked.connect(lambda checked, k=key: self.switch_script(k))
            button_layout.addWidget(btn)
            self.buttons[key] = btn

        self.update_script_buttons()

    def update_script_buttons(self):
        for key, btn in self.buttons.items():
            btn.setEnabled(key != "ivr")
            btn.setEnabled(key != "ivr_to_inc")
            btn.setEnabled(key != "ivr_lv")
            btn.setEnabled(key != "inc")
            btn.setEnabled(key != "inc_to_ivr")
            btn.setEnabled(key != "del")
            btn.setEnabled(key != None)


    def switch_script(self, script_name):
        if script_name not in self.scripts:
            return
        self.current_script = script_name
        script_info = self.scripts[script_name]

        self.title_label.setText(script_info["title"])

        self.context_label.setText(script_info["context_label"])
        self.context_field.setPlaceholderText(script_info["context_hint"])
        self.context_field.setText("")

        self.client_label.setText(script_info["client_label"])
        self.client_field.setPlaceholderText(script_info["client_hint"])
        self.client_field.setText("")

        self.prefix_label.setText(script_info["prefix_label"])
        self.prefix_field.setPlaceholderText(script_info["prefix_hint"])
        self.prefix_field.setText("")

        self.main_label.setText(script_info["main_label"])
        self.main_field.setPlaceholderText(script_info["ivr_hint"])
        self.main_field.setText("")

        self.output_field.clear()
        self.numbers_field.clear()

        self.update_script_buttons()

    def generate_query(self):
        try:
            input_text = self.numbers_field.toPlainText().strip()
            if not input_text:
                return
            func = getattr(self, f"generate_{self.current_script}_query")
            if func:
                func()
            else:
                self.output_field.setPlainText("Функция генерации не найдена")
        except Exception as e:
            self.output_field.setPlainText(f"Ошибка: {str(e)}")

    def generate_ivr_query(self):
        try:
            context = self.context_field.text()
            client = self.client_field.text()
            ivr_file = self.main_field.text()
            numbers = self.numbers_field.toPlainText().splitlines()

            res = "INSERT INTO extensions (context, exten, priority, app, appdata) VALUES\n"
            for number in numbers:
                n = number.strip()
                if not n:
                    continue
                res += f"('{context}', '{n}', '1', 'Log', 'NOTICE, incomming for {client}'),\n"
                res += f"('{context}', '{n}', '2', 'Answer', ''),\n"
                res += f"('{context}', '{n}', '3', 'Wait', '1'),\n"
                res += f"('{context}', '{n}', '4', 'Playback', '{ivr_file},skip'),\n"
                res += f"('{context}', '{n}', '5', 'Hangup', ''),\n"
            res = res.rstrip(",\n") + ";"
            self.output_field.setPlainText(res)
        except Exception as e:
            self.output_field.setPlainText(f"Ошибка: {str(e)}")

    def generate_ivr_to_inc_query(self):
        try:
            context = self.context_field.text()
            prefix = self.prefix_field.text()
            numbers = self.numbers_field.toPlainText().splitlines()

            res = ""
            for number in numbers:
                n = number.strip()
                if not n:
                    continue
                res += f"DELETE FROM extensions WHERE exten = '{n}' AND context = '{context}';\n"
                res += f"INSERT INTO extensions (context, exten, priority, app, appdata) VALUES\n"
                res += f"('{context}', '{n}', '1', 'Log', 'NOTICE, incomming'),\n"
                res += f"('{context}', '{n}', '2', 'Dial', 'SIP/mediacore/{prefix}${{{n}}}',60),\n"
                res += f"('{context}', '{n}', '3', 'Hangup', '');\n"
            self.output_field.setPlainText(res)
        except Exception as e:
            self.output_field.setPlainText(f"Ошибка: {str(e)}")

    def generate_ivr_lv_query(self):
        try:
            input_text = self.numbers_field.text.strip()
            if not input_text:
                return
            context = self.context_field.text
            client = self.client_field.text
            ivr_file = self.main_field.text
            numbers = self.numbers_field.text.splitlines()

            res = "INSERT INTO extensions (context, exten, priority, app, appdata) VALUES"
            for number in numbers:
                res += f"('{context}', '{number.strip()}', '1', 'Log', 'NOTICE, incomming for {client}'),"
                res += f"('{context}', '{number.strip()}', '2', 'Answer', ''),"
                res += f"('{context}', '{number.strip()}', '3', 'Wait', '1'),"
                res += f"('{context}', '{number.strip()}', '4', 'Playback', '{ivr_file},skip'),"
                res += f"('{context}', '{number.strip()}', '5', 'Hangup', ''),"
            res = res[:-1] + ';'
            self.output_field.text = res
        except Exception as e:
            self.output_field.text = f"Ошибка: {str(e)}"

    def generate_inc_query(self):
        try:
            context = self.context_field.text()
            client = self.client_field.text()
            prefix = self.prefix_field.text()
            numbers = self.numbers_field.toPlainText().splitlines()

            res = "INSERT INTO extensions (context, exten, priority, app, appdata) VALUES\n"
            for number in numbers:
                n = number.strip()
                if not n:
                    continue
                res += f"('{context}', '{n}', '1', 'Log', 'NOTICE, for {client}'),\n"
                res += f"('{context}', '{n}', '2', 'Dial', 'SIP/mediacore/{prefix}${{{n}}}',60),\n"
                res += f"('{context}', '{n}', '3', 'Hangup', ''),\n"
            res = res.rstrip(",\n") + ";"
            self.output_field.setPlainText(res)
        except Exception as e:
            self.output_field.setPlainText(f"Ошибка: {str(e)}")

    def generate_inc_to_ivr_query(self):
        try:
            context = self.context_field.text()
            ivr_file = self.main_field.text()
            numbers = self.numbers_field.toPlainText().splitlines()

            res = ""
            for number in numbers:
                n = number.strip()
                if not n:
                    continue
                res += f"DELETE FROM extensions WHERE exten = '{n}' AND context = '{context}';\n"
                res += f"INSERT INTO extensions (context, exten, priority, app, appdata) VALUES\n"
                res += f"('{context}', '{n}', '1', 'Log', 'NOTICE, incomming'),\n"
                res += f"('{context}', '{n}', '2', 'Answer', ''),\n"
                res += f"('{context}', '{n}', '3', 'Wait', '1'),\n"
                res += f"('{context}', '{n}', '4', 'Playback', '{ivr_file},skip'),\n"
                res += f"('{context}', '{n}', '5', 'Hangup', '');\n"
            self.output_field.setPlainText(res)
        except Exception as e:
            self.output_field.setPlainText(f"Ошибка: {str(e)}")

    def generate_del_query(self):
        try:
            context = self.context_field.text()
            numbers = self.numbers_field.toPlainText().splitlines()

            res = ""
            for number in numbers:
                n = number.strip()
                if not n:
                    continue
                res += f"DELETE FROM extensions WHERE exten = '{n}' AND context = '{context}';\n"
            self.output_field.setPlainText(res)
        except Exception as e:
            self.output_field.setPlainText(f"Ошибка: {str(e)}")

    def switch_script(self, script_name):
        self.current_script = script_name
        script_info = self.scripts[script_name]

        self.title_label.setText(script_info["title"])
        self.context_label.setText(script_info["context_label"])
        self.context_field.setPlaceholderText(script_info["context_hint"])
        self.client_label.setText(script_info["client_label"])
        self.client_field.setPlaceholderText(script_info["client_hint"])
        self.prefix_label.setText(script_info["prefix_label"])
        self.prefix_field.setPlaceholderText(script_info["prefix_hint"])
        self.main_label.setText(script_info["main_label"])
        self.main_field.setPlaceholderText(script_info["ivr_hint"])