import requests
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QPlainTextEdit, QApplication
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QCompleter

class CurrencyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.api_key = "2f8f8942a6f5764cff8c55faf7ef44c3"
        self.available_currencies = []
        self.is_loading = False
        
        self.init_ui()
        self.update_rates()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # Заголовок
        self.title_label = QLabel("Конвертер валют")
        font = self.title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        main_layout.addWidget(self.title_label)

        # Сумма
        self.amount_label = QLabel("Сумма:")
        main_layout.addWidget(self.amount_label)
        
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("Введите сумму")
        self.amount_edit.returnPressed.connect(self.convert)
        main_layout.addWidget(self.amount_edit)

        # Валюты с иконкой конвертации
        currencies_layout = QHBoxLayout()
        currencies_layout.setSpacing(15)
        main_layout.addLayout(currencies_layout)
        
        # Из
        self.from_edit = QLineEdit()
        self.from_edit.setPlaceholderText("Из валюты...")
        self.from_edit.setMinimumWidth(100)
        currencies_layout.addWidget(self.from_edit)
        
        # Стрелка конвертации (кликабельная)
        self.arrow_label = QLabel(" ⇆ ")
        font = self.arrow_label.font()
        font.setPointSize(30)
        self.arrow_label.setFont(font)
        self.arrow_label.setAlignment(Qt.AlignCenter)
        self.arrow_label.setCursor(Qt.PointingHandCursor)  # курсор руки
        self.arrow_label.mousePressEvent = self.swap_currencies  # клик меняет валюты
        currencies_layout.addWidget(self.arrow_label)
        
        # В
        self.to_edit = QLineEdit()
        self.to_edit.setPlaceholderText("В валюту...")
        self.to_edit.setMinimumWidth(100)
        currencies_layout.addWidget(self.to_edit)

        # Результат (чисто число)
        self.result_field = QPlainTextEdit()
        self.result_field.setReadOnly(True)
        self.result_field.setMaximumHeight(60)
        self.result_field.installEventFilter(self)
        main_layout.addWidget(self.result_field)

        # Инфо о курсах (внизу, серый фон)
        self.info_field = QPlainTextEdit()
        self.info_field.setReadOnly(True)
        self.info_field.setMaximumHeight(60)
        main_layout.addWidget(self.info_field)

        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # КНОПКИ ВНИЗУ (как в других скриптах)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        main_layout.addLayout(button_layout)

        self.update_button = QPushButton("Обновить курсы")
        self.update_button.clicked.connect(self.update_rates)
        button_layout.addWidget(self.update_button)
        
        self.convert_button = QPushButton("Конвертировать")
        self.convert_button.clicked.connect(self.convert)
        button_layout.addWidget(self.convert_button)
        
        self.back_button = QPushButton("Назад")
        button_layout.addWidget(self.back_button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer)

    def eventFilter(self, obj, event):
        if obj == self.result_field and event.type() == QEvent.KeyPress:
            if event.matches(QKeySequence.Copy):
                text = self.result_field.toPlainText()
                QApplication.clipboard().setText(text)
                return True
        return super().eventFilter(obj, event)

    def swap_currencies(self, event):
        """Меняет валюты местами при клике на стрелку"""
        from_curr = self.from_edit.text().strip()
        to_curr = self.to_edit.text().strip()
        
        self.from_edit.setText(to_curr)
        self.to_edit.setText(from_curr)
        
        # Очищаем результат при смене валют
        self.result_field.clear()

    def update_rates(self):
        """Загружаем курсы через /live endpoint"""
        if self.is_loading:
            return
            
        self.is_loading = True
        self.update_button.setText("Загрузка...")
        self.update_button.setEnabled(False)
        
        try:
            url = "http://api.currencylayer.com/live"
            params = {
                'access_key': self.api_key,
                'format': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success', False):
                raise Exception(f"API ошибка: {data.get('error', {}).get('info', 'Неизвестная ошибка')}")
            
            # Парсим quotes в словарь курсов относительно USD
            self.rates_data = data
            self.available_currencies = sorted([
                quote[3:] for quote in data['quotes'].keys()  # убираем "USD" префикс
            ])
            
            # ★ НАДЁЖНЫЙ АВТОКОМПЛИТ ★
            currencies_list = self.available_currencies[:]
            
            # Настраиваем комплитеры ПОСЛЕ загрузки валют
            from_completer = QCompleter(currencies_list)
            from_completer.setCaseSensitivity(Qt.CaseInsensitive)
            from_completer.setFilterMode(Qt.MatchContains)
            self.from_edit.setCompleter(from_completer)
            
            # ★ СТИЛИЗАЦИЯ ★
            from_popup = from_completer.popup()
            from_popup.setObjectName("currencyCompleter")
            from_popup.setStyleSheet("""
                QAbstractItemView#currencyCompleter {
                    background-color: #444444;
                    color: #FF6666;
                    border-radius: 10px;
                    border: none;
                    outline: none;
                    padding: 5px;
                }

                QAbstractItemView#currencyCompleter::item {
                    background-color: transparent;
                    color: #FF6666;
                    padding: 8px 24px;
                    margin: 4px 0;
                    border-radius: 10px;
                }

                QAbstractItemView#currencyCompleter::item:selected {
                    background-color: #555555;
                    color: white;
                }

                QAbstractItemView#currencyCompleter::item:hover {
                    background-color: #555555;
                    color: white;
                }
            """)
            
            # To completer
            to_completer = QCompleter(currencies_list)
            to_completer.setCaseSensitivity(Qt.CaseInsensitive)
            to_completer.setFilterMode(Qt.MatchContains)
            self.to_edit.setCompleter(to_completer)
            
            # Стилизация второго комплитера
            to_popup = to_completer.popup()
            to_popup.setObjectName("currencyCompleter")
            to_popup.setStyleSheet("""
                QAbstractItemView#currencyCompleter {
                    background-color: #444444;
                    color: #FF6666;
                    border-radius: 10px;
                    border: none;
                    outline: none;
                    padding: 5px;
                }

                QAbstractItemView#currencyCompleter::item {
                    background-color: transparent;
                    color: #FF6666;
                    padding: 8px 24px;
                    margin: 4px 0;
                    border-radius: 10px;
                }

                QAbstractItemView#currencyCompleter::item:selected {
                    background-color: #555555;
                    color: white;
                }

                QAbstractItemView#currencyCompleter::item:hover {
                    background-color: #555555;
                    color: white;
                }
            """)
            
            # Популярные валюты по умолчанию
            self.from_edit.setText('RUB' if 'RUB' in self.available_currencies else 'USD')
            self.to_edit.setText('USD' if 'USD' in self.available_currencies else 'EUR')
            
            self.result_field.clear()
            self.info_field.setPlainText("Курсы валют обновлены")
            
        except requests.exceptions.RequestException as e:
            self.info_field.setPlainText(f"Ошибка сети: {str(e)}")
        except Exception as e:
            self.info_field.setPlainText(f"Ошибка: {str(e)}")
        finally:
            self.is_loading = False
            self.update_button.setText("Обновить курсы")
            self.update_button.setEnabled(True)

    def convert(self):
        """Конвертируем через /convert endpoint"""
        if not hasattr(self, 'rates_data') or not self.available_currencies:
            self.info_field.setPlainText("Сначала обновите курсы")
            return
        
        try:
            # Парсим сумму (запятая → точка)
            amount_text = self.amount_edit.text().strip().replace(',', '.')
            if not amount_text:
                raise ValueError("Введите сумму")
            amount = float(amount_text)
            
            from_curr = self.from_edit.text().strip().upper()
            to_curr = self.to_edit.text().strip().upper()
            
            if not from_curr or not to_curr:
                raise ValueError("Введите валюты")
            
            # Используем /convert endpoint
            url = "http://api.currencylayer.com/convert"
            params = {
                'access_key': self.api_key,
                'from': from_curr,
                'to': to_curr,
                'amount': amount,
                'format': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success', False):
                raise Exception(f"API ошибка: {data.get('error', {}).get('info', 'Неизвестная ошибка')}")
            
            result = data['result']
            
            # Чистый результат в основном поле
            self.result_field.setPlainText(f"{result:.8g}")
            
            # Инфо о курсе внизу
            timestamp = data.get('info', {}).get('timestamp', 0)
            self.info_field.setPlainText(f"{self._format_timestamp(timestamp)}")
            
        except ValueError as e:
            self.result_field.setPlainText("")
            self.info_field.setPlainText(f"Ошибка: {str(e)}")
        except requests.exceptions.RequestException as e:
            self.result_field.setPlainText("")
            self.info_field.setPlainText(f"Ошибка сети: {str(e)}")
        except Exception as e:
            self.result_field.setPlainText("")
            self.info_field.setPlainText(f"Ошибка: {str(e)}")

    def _format_timestamp(self, timestamp):
        """Форматируем timestamp в читаемую дату"""
        try:
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%d.%m.%Y %H:%M")
        except:
            return "неизвестно"
