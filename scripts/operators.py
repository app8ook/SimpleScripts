import os
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QMessageBox, QProgressBar, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class OperatorProcessorThread(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, calls_file, codes_file, output_dir='output_operators'):
        super().__init__()
        self.calls_file = calls_file
        self.codes_file = codes_file
        self.output_dir = output_dir

    def run(self):
        try:
            self.log.emit(f"Загрузка справочника: {self.codes_file}")
            codes_df = pd.read_excel(self.codes_file, header=None)
            codes_df.columns = ['operator', 'code']
            codes_df['code'] = codes_df['code'].astype(str).str.strip()
            codes_df['operator'] = codes_df['operator'].astype(str).str.strip()
            codes_df = codes_df.sort_values(by='code', key=lambda x: x.str.len(), ascending=False).reset_index(drop=True)
            codes_list = list(zip(codes_df['code'], codes_df['operator']))

            self.log.emit(f"Загрузка номеров: {self.calls_file}")
            calls_df = pd.read_excel(self.calls_file, header=None)
            calls_df.columns = ['number']
            calls_df['number'] = calls_df['number'].astype(str).str.strip()

            def find_operator(phone):
                phone_str = str(phone)
                for code, operator in codes_list:
                    if phone_str.startswith(code):
                        return operator
                return 'Прочие'

            total = len(calls_df)
            calls_df['operator'] = ''
            for i, number in enumerate(calls_df['number']):
                calls_df.at[i, 'operator'] = find_operator(number)
                if i % 10 == 0 or i == total - 1:
                    self.progress.emit(int(i / total * 100))

            os.makedirs(self.output_dir, exist_ok=True)

            for operator, group in calls_df.groupby('operator'):
                safe_operator = "".join(c for c in operator if c.isalnum() or c in " _-").rstrip()
                filename = os.path.join(self.output_dir, f"{safe_operator}.txt")
                group['number'].to_csv(filename, index=False, header=False)
                self.log.emit(f'{operator} — {len(group)}')

            self.log.emit(f"Файлы успешно созданы в папке {self.output_dir}")
        except Exception as e:
            self.log.emit(f"Ошибка: {str(e)}")
        self.finished.emit()

class OperatorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.calls_file = None
        self.codes_file = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        self.calls_preview = QTextEdit()
        self.calls_preview.setReadOnly(True)
        self.calls_preview.setPlaceholderText(
            "Пример данных из файла номеров (В первом столбце должны быть номера)\n"
            "79034196864 | \n"
            "79097567562 | \n"
            "79373888188 | \n"
            "79195926335 | \n"
            "79991990004 | \n")
        main_layout.addWidget(QLabel("Превью номеров:"))
        main_layout.addWidget(self.calls_preview, 1)

        self.codes_preview = QTextEdit()
        self.codes_preview.setReadOnly(True)
        self.codes_preview.setPlaceholderText(
            "Пример данных из файла кодов"
            "Билайн | 7903 | \n"
            "Билайн | 7909 | \n"
            "МегаФон | 7937 | \n"
            "МТС | 7919 | \n"
            "И т.д.\n")
        main_layout.addWidget(QLabel("Превью кодов операторов:"))
        main_layout.addWidget(self.codes_preview, 1)

        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText(
            "Пример обработанных данных"
            "Билайн — 2\n"
            "МТС — 1\n"
            "МегаФон — 1\n"
            "Прочие — 1\n"
            "*Так же создаются текстовые файлы для разбиения номеров по операторам\n")
        main_layout.addWidget(QLabel("Лог обработки:"))
        main_layout.addWidget(self.log_output, 2)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.load_calls_btn = QPushButton("Выбрать файл номеров")
        self.load_calls_btn.clicked.connect(self.load_calls_file)
        button_layout.addWidget(self.load_calls_btn)

        self.load_codes_btn = QPushButton("Выбрать файл кодов")
        self.load_codes_btn.clicked.connect(self.load_codes_file)
        button_layout.addWidget(self.load_codes_btn)

        self.process_btn = QPushButton("Обработка")
        self.process_btn.setEnabled(False)
        self.process_btn.clicked.connect(self.start_processing)
        button_layout.addWidget(self.process_btn)

        self.back_button = QPushButton("Назад")
        button_layout.addWidget(self.back_button)
        main_layout.addLayout(button_layout)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer)

    def load_calls_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите файл с номерами", "", "Excel Files (*.xlsx *.xls)")
        if path:
            self.calls_file = path
            self.show_preview(path, self.calls_preview)
            self.check_ready()

    def load_codes_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите файл с кодами операторов", "", "Excel Files (*.xlsx *.xls)")
        if path:
            self.codes_file = path
            self.show_preview(path, self.codes_preview)
            self.check_ready()

    def show_preview(self, filepath, widget, max_rows=10):
        try:
            df = pd.read_excel(filepath, header=None)
            preview_text = df.head(max_rows).to_string(index=False, header=False)
            widget.setPlainText(preview_text)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить файл:\n{str(e)}")

    def check_ready(self):
        self.process_btn.setEnabled(bool(self.calls_file and self.codes_file))

    def start_processing(self):
        self.log_output.clear()
        self.progress_bar.setValue(0)
        self.thread = OperatorProcessorThread(self.calls_file, self.codes_file)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.log.connect(self.append_log)
        self.thread.finished.connect(self.processing_finished)
        self.thread.start()
        self.process_btn.setEnabled(False)

    def append_log(self, message):
        self.log_output.append(message)

    def processing_finished(self):
        self.append_log("Обработка завершена.")
        self.process_btn.setEnabled(True)