import json
from pathlib import Path
import urllib.request
from urllib.error import URLError, HTTPError

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QPlainTextEdit, QApplication
)
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QKeySequence

from Token import TOKENFORBD

class CountryNetwork(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_data = None
        self.base_loaded = False
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        main_layout.addWidget(QLabel("Введите номера (по одному в строке):"))
        self.numbers_input = QPlainTextEdit()
        main_layout.addWidget(self.numbers_input, 1)

        main_layout.addWidget(QLabel("Результат:"))
        self.result_output = QPlainTextEdit()
        self.result_output.setReadOnly(True)
        main_layout.addWidget(self.result_output, 2)

        self.result_output.installEventFilter(self)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        main_layout.addLayout(button_layout)

        self.load_base_button = QPushButton("Прочитать базу")
        self.load_base_button.clicked.connect(self.load_base_from_file)
        button_layout.addWidget(self.load_base_button)

        self.process_button = QPushButton("Обработать")
        self.process_button.clicked.connect(self.process_numbers)
        button_layout.addWidget(self.process_button)

        self.back_button = QPushButton("Назад")
        button_layout.addWidget(self.back_button)

        button_layout.addStretch(1)

    def eventFilter(self, obj, event):
        if obj == self.result_output and event.type() == QEvent.KeyPress:
            if event.matches(QKeySequence.Copy):
                QApplication.clipboard().setText(self.result_output.toPlainText())
                return True
        return super().eventFilter(obj, event)

    def validate_base_data(self, data):
        required_fields = ["country", "network", "iso", "mcc", "mnc", "plmn", "country_code"]
        bad_rows = []

        for i, row in enumerate(data):
            problems = []

            for field in required_fields:
                value = str(row.get(field, "")).strip()
                if not value:
                    problems.append(f"{field} empty")

            mcc = str(row.get("mcc", "")).strip()
            mnc = str(row.get("mnc", "")).strip()
            plmn = str(row.get("plmn", "")).strip()

            if mcc and not mcc.isdigit():
                problems.append("mcc not numeric")

            if mnc and not mnc.isdigit():
                problems.append("mnc not numeric")

            if plmn and "-" not in plmn:
                problems.append("plmn invalid")

            if problems:
                bad_rows.append((i, row, problems))

        return bad_rows

    def load_base_from_file(self):
            url = "https://raw.githubusercontent.com/app8ook/countrycodes/main/Data.json"
            
            headers = {
                'User-Agent': 'SimpleScripts/0.6',
                'Authorization': f'Bearer {TOKENFORBD}'
            }
            try:
                # Запрашиваем данные по ссылке с таймаутом в 10 секунд
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = response.read().decode('utf-8')
                    self.base_data = json.loads(data)
                    
            except HTTPError as e:
                self.base_data = None
                self.base_loaded = False
                self.result_output.setPlainText(f"HTTP Ошибка сервера при скачивании базы: {e.code}")
                return
            except URLError as e:
                self.base_data = None
                self.base_loaded = False
                self.result_output.setPlainText(f"Ошибка сети (нет интернета или недоступен URL): {e.reason}")
                return
            except json.JSONDecodeError:
                self.base_data = None
                self.base_loaded = False
                self.result_output.setPlainText("Ошибка: Неверный формат JSON по ссылке")
                return
            except Exception as e:
                self.base_data = None
                self.base_loaded = False
                self.result_output.setPlainText(f"Неизвестная ошибка: {e}")
                return

            # Оригинальная проверка формата скачанных данных
            bad_rows = self.validate_base_data(self.base_data)

            if bad_rows:
                self.base_loaded = False
                lines = [f"Ошибка формата данных: {len(bad_rows)} проблемных строк"]
                for idx, row, problems in bad_rows[:20]:
                    lines.append(f"#{idx + 1}: {', '.join(problems)}")
                self.result_output.setPlainText("\n".join(lines))
                return

            self.base_loaded = True
            self.result_output.setPlainText(f"База загружена по сети: {len(self.base_data)} записей")

    def process_numbers(self):
        if not self.base_loaded or not self.base_data:
            self.result_output.setPlainText("Нет базы для взаимодействия")
            return

        numbers = [line.strip() for line in self.numbers_input.toPlainText().splitlines() if line.strip()]
        if not numbers:
            self.result_output.setPlainText("Введите номера в поле для обработки")
            return

        results = []
        for num in numbers:
            results.append(self.process_one_number(num))

        self.result_output.setPlainText("\n".join(results))

    def process_one_number(self, number):
        num = number.strip().lstrip("+")
        matches = self.find_matches(num)

        if not matches:
            return f"{number}; Неизвестно; ; ;"

        default_row = None
        best_row = None
        best_len = -1

        for row in matches:
            mnc = str(row.get("mnc", "")).strip()
            if mnc in ("0", "000") and default_row is None:
                default_row = row
            code = str(row.get("network_code", "")).strip()
            if code and num.startswith(str(row.get("country_code", "")) + code):
                if len(code) > best_len:
                    best_len = len(code)
                    best_row = row

        row = best_row or default_row or matches[0]
        country = str(row.get("country", "")).strip()
        network = str(row.get("network", "")).strip()
        iso = str(row.get("iso", "")).strip()
        mcc = str(row.get("mcc", "")).strip()
        mnc = str(row.get("mnc", "")).strip()

        return f"{number}; {country}; {network}; {iso}; {mcc}-{mnc}"

    def find_matches(self, number):
        matches = []
        for row in self.base_data:
            cc = str(row.get("country_code", "")).strip()
            if cc and number.startswith(cc):
                matches.append(row)
        return matches