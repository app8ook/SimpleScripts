import sys, os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStackedWidget, QHBoxLayout, QLabel, QPushButton, QWidget, QSizePolicy, QSpacerItem, QVBoxLayout

from scripts.dublicates import DuplicatesWidget
from scripts.doubledata import DoubledataWidget
from scripts.prefix import PrefixWidget
from scripts.aster import AsterWidget
from scripts.numbers import NumWidget
from scripts.mysql import MysqlWidget
from scripts.beeline import BeelineWidget
from scripts.operators import OperatorWidget
from scripts.countrycode import CountryCodeWidget
from scripts.about import AboutWidget

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

STYLE_FILE = resource_path("style.qss")
UI_FILE = resource_path("interface.ui")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_FILE, self)

        self.resize(800, 800)
        self.setMinimumSize(600, 600)

        self.category_buttons = {
            'Скрипт1': self.pushButton_1, 
            'Скрипт2': self.pushButton_2, 
            'Скрипт3': self.pushButton_3, 
            'Скрипт4': self.pushButton_4, 
            'Скрипт5': self.pushButton_5, 
            'Скрипт6': self.pushButton_6, 
            'Скрипт7': self.pushButton_7,
            'Скрипт8': self.pushButton_8,
            'Скрипт10': self.pushButton_10,
            'Скрипт9': self.pushButton_9
        }

        self.category_group = QtWidgets.QButtonGroup()
        self.category_group.setExclusive(True)
        for btn in self.category_buttons.values():
            btn.setCheckable(True)
            self.category_group.addButton(btn)

        self.script_container = QStackedWidget()
        self.centralLayout.addWidget(self.script_container)

        self.script1_widget = DuplicatesWidget()
        self.script_container.addWidget(self.script1_widget)
        self.script1_widget.back_button.clicked.connect(self.show_main_menu)
        
        self.script2_widget = DoubledataWidget()
        self.script_container.addWidget(self.script2_widget)
        self.script2_widget.back_button.clicked.connect(self.show_main_menu)
        
        self.script3_widget = PrefixWidget()
        self.script_container.addWidget(self.script3_widget)
        self.script3_widget.back_button.clicked.connect(self.show_main_menu)

        self.script4_widget = AsterWidget()
        self.script_container.addWidget(self.script4_widget)
        self.script4_widget.back_button.clicked.connect(self.show_main_menu)
        
        self.script5_widget = NumWidget()
        self.script_container.addWidget(self.script5_widget)
        self.script5_widget.back_button.clicked.connect(self.show_main_menu)

        self.script6_widget = MysqlWidget()
        self.script_container.addWidget(self.script6_widget)
        self.script6_widget.back_button.clicked.connect(self.show_main_menu)

        self.script7_widget = BeelineWidget()
        self.script_container.addWidget(self.script7_widget)
        self.script7_widget.back_button.clicked.connect(self.show_main_menu)

        self.script8_widget = OperatorWidget()
        self.script_container.addWidget(self.script8_widget)
        self.script8_widget.back_button.clicked.connect(self.show_main_menu)

        self.script10_widget = CountryCodeWidget()
        self.script_container.addWidget(self.script10_widget)
        self.script10_widget.back_button.clicked.connect(self.show_main_menu)

        self.script9_widget = AboutWidget()
        self.script_container.addWidget(self.script9_widget)
        self.script9_widget.back_button.clicked.connect(self.show_main_menu)

        self.show_main_menu()

        for name, btn in self.category_buttons.items():
            btn.clicked.connect(lambda checked, n=name: self.change_category(n))

        buttons_layout = self.mainMenuWidget.layout()

        buttons_container = QWidget()
        buttons_container.setLayout(buttons_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(buttons_container)
        main_layout.addStretch()

        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        footer_layout.addWidget(QLabel("Версия: 0.4"))
        footer_layout.addStretch()

        main_layout.addLayout(footer_layout)

        self.mainMenuWidget.setLayout(main_layout)

    def change_category(self, category_name):
        widget_attr_name = category_name.lower().replace('скрипт', 'script') + '_widget'
        widget = getattr(self, widget_attr_name, None)
        if widget:
            self.script_container.setCurrentWidget(widget)
            self.script_container.show()
            self.mainMenuWidget.hide()
        else:
            self.show_main_menu()

    def show_main_menu(self):
        self.script_container.hide()
        self.mainMenuWidget.show()

def load_stylesheet(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    QtWidgets.QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    app = QtWidgets.QApplication(sys.argv)
    style = load_stylesheet(STYLE_FILE)
    app.setStyleSheet(style)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())