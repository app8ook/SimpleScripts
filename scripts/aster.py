from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt

class AsterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scripts = {
            "inc": {
                "title": "INC",
                "prefix_label": "Префикс:",
                "prefix_hint": "Введите префикс",
                "comment_label": "Комментарий:",
                "comment_hint": "Введите комментарий",
                "generate_function": self.generate_inc_dialplan
            },
            "noinc": {
                "title": "NOINC",
                "prefix_label": "",
                "prefix_hint": "",
                "comment_label": "Комментарий:",
                "comment_hint": "Введите комментарий",
                "generate_function": self.generate_noinc_dialplan
            }
        }
        self.current_script = "inc"

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        self.title_label = QLabel(self.scripts[self.current_script]["title"])
        font = self.title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        main_layout.addWidget(self.title_label)

        self.input_label = QLabel("Ввод:")
        main_layout.addWidget(self.input_label)

        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Введите текст")
        main_layout.addWidget(self.input_field)

        self.prefix_label = QLabel(self.scripts[self.current_script]["prefix_label"])
        main_layout.addWidget(self.prefix_label)

        self.prefix_field = QTextEdit()
        self.prefix_field.setFixedHeight(40)
        self.prefix_field.setPlaceholderText(self.scripts[self.current_script]["prefix_hint"])
        main_layout.addWidget(self.prefix_field)

        self.comment_label = QLabel(self.scripts[self.current_script]["comment_label"])
        main_layout.addWidget(self.comment_label)

        self.comment_field = QTextEdit()
        self.comment_field.setFixedHeight(40)
        self.comment_field.setPlaceholderText(self.scripts[self.current_script]["comment_hint"])
        main_layout.addWidget(self.comment_field)

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
        self.generate_button.clicked.connect(self.generate_dialplan)
        button_layout.addWidget(self.generate_button)

        self.back_button = QPushButton("Назад")
        button_layout.addWidget(self.back_button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer)

        self.inc_button = QPushButton("INC")
        self.inc_button.clicked.connect(lambda: self.switch_script("inc"))
        button_layout.addWidget(self.inc_button)

        self.noinc_button = QPushButton("NOINC")
        self.noinc_button.clicked.connect(lambda: self.switch_script("noinc"))
        button_layout.addWidget(self.noinc_button)

        self.update_script_buttons()

    def update_script_buttons(self):
        self.inc_button.setEnabled(self.current_script != "inc")
        self.noinc_button.setEnabled(self.current_script != "noinc")

    def switch_script(self, script_name):
        if script_name not in self.scripts:
            return
        self.current_script = script_name
        script_info = self.scripts[script_name]

        self.title_label.setText(script_info["title"])
        self.prefix_label.setText(script_info["prefix_label"])
        self.prefix_field.setPlaceholderText(script_info["prefix_hint"])
        self.comment_label.setText(script_info["comment_label"])
        self.comment_field.setPlaceholderText(script_info["comment_hint"])

        self.output_field.clear()
        if script_name == "noinc":
            self.prefix_field.setDisabled(True)
            self.prefix_field.clear()
        else:
            self.prefix_field.setDisabled(False)

        self.update_script_buttons()

    def generate_inc_dialplan(self):
        numbers = self.input_field.toPlainText().strip().splitlines()
        prefix = self.prefix_field.toPlainText().strip()
        comment = self.comment_field.toPlainText().strip()
        dialplan_entries = []
        for number in numbers:
            entry = (
                f"exten => {number},1,Log(NOTICE, Incoming for {comment})\n"
                f" same => n,Dial(SIP/mediacore/{prefix}${number},60)\n"
                f" same => n,Hangup()"
            )
            dialplan_entries.append(entry)
        output = "\n\n".join(dialplan_entries)
        output += f"\n\nУспешно обработано номеров: {len(numbers)}"
        return output

    def generate_noinc_dialplan(self):
        numbers = self.input_field.toPlainText().strip().splitlines()
        comment = self.comment_field.toPlainText().strip()
        dialplan_entries = []
        for number in numbers:
            entry = (
                f"exten => {number},1,Log(NOTICE, incoming for {comment})\n"
                " same => n,Answer()\n"
                " same => n,Wait(1)\n"
                " same => n,Playback(/var/lib/asterisk/sounds/lv/IVR,skip)\n"
                " same => n,Hangup()"
            )
            dialplan_entries.append(entry)
        output = "\n\n".join(dialplan_entries)
        output += f"\n\nУспешно обработано номеров: {len(numbers)}"
        return output

    def generate_dialplan(self):
        input_text = self.input_field.toPlainText().strip()
        if not input_text:
            self.output_field.setPlainText("Пожалуйста, введите номера.")
            return

        if self.current_script == "inc":
            output = self.generate_inc_dialplan()
        else:
            output = self.generate_noinc_dialplan()

        self.output_field.setPlainText(output)
