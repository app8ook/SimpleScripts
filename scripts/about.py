from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QPushButton, QTextEdit, QSizePolicy
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

class AboutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_file = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        self.label = QLabel(
            "Программа написана с целью оптимизировать работу,\n"
            "с помощью различных скриптов, для работы в телефонии\n"
            "(Для компании Zorra)\n"
            "\n"
            "Для поддержки автора, перейдите по кнопке 'Сайт автора'\n"
        )
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setMinimumHeight(300)
        main_layout.addWidget(self.label)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        main_layout.addLayout(button_layout)

        self.link_btn = QPushButton('Сайт автора')
        self.link_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://app8ook.github.io')))
        button_layout.addWidget(self.link_btn)

        self.back_button = QPushButton("Назад")
        button_layout.addWidget(self.back_button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer)