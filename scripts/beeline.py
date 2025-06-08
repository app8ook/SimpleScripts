import os, xlrd, openpyxl
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit,
    QSizePolicy, QSpacerItem, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class BeelineProcessorThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, input_file):
        super().__init__()
        self.input_file = input_file

    def run(self):
        try:
            # Открываем .xls файл через xlrd
            wb_input = xlrd.open_workbook(self.input_file)
            ws_input = wb_input.sheet_by_index(0)

            output_file = os.path.join(os.path.dirname(self.input_file), 'output.xlsx')
            wb_output = openpyxl.Workbook()
            ws_output = wb_output.active

            headers = ['DEST', 'COUNTRY CODE', 'ROLLUP', 'RATE', 'MC', 'CI', 'FT']
            ws_output.append(headers)

            total = ws_input.nrows - 1  # минус заголовок
            if total <= 0:
                self.error.emit("Входной файл пустой или содержит только заголовок")
                return

            for i in range(1, ws_input.nrows):
                row = ws_input.row_values(i)
                dest = row[0]
                country_code = str(row[1]) if row[1] is not None else ''
                rollup = str(row[2]) if row[2] is not None else ''
                
                # Обработка значения rate — xlrd возвращает числа как float
                rate = '0.0000'
                if row[3] is not None and row[3] != '':
                    try:
                        rate = f"{float(row[3]):.4f}"
                    except ValueError:
                        rate = '0.0000'

                processed_data = []

                if rollup:
                    rollup_values = []
                    for part in rollup.split(','):
                        part = part.strip()
                        if '-' in part:
                            start_end = part.split('-')
                            if len(start_end) == 2 and all(x.strip().isdigit() for x in start_end):
                                start, end = map(int, start_end)
                                rollup_values.extend(range(start, end + 1))
                        else:
                            if part.isdigit():
                                rollup_values.append(int(part))

                    for value in rollup_values:
                        processed_data.append([dest, country_code, value, rate, 1, 1, 0])
                else:
                    processed_data.append([dest, country_code, '', rate, 1, 1, 0])

                for data_row in processed_data:
                    dest_val, country_code_val, rollup_val, rate_val, mc_val, ci_val, ft_val = data_row

                    if isinstance(rollup_val, int):
                        rollup_val_str = str(rollup_val)
                        original_rollups = [part.strip() for part in rollup.split(',')]
                        if any(r.lstrip('0') == rollup_val_str for r in original_rollups):
                            rollup_val_str = str(rollup_val)
                        else:
                            rollup_val_str = str(rollup_val).zfill(2)
                    else:
                        rollup_val_str = ''

                    ws_output.append([dest_val, country_code_val, rollup_val_str, rate_val, mc_val, ci_val, ft_val])

                progress_percent = int(i / total * 100)
                self.progress.emit(progress_percent)

            wb_output.save(output_file)
            self.finished.emit(output_file)

        except Exception as e:
            self.error.emit(str(e))

class BeelineWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_file = None
        self.thread = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        self.label = QLabel(
            "Скрипт для обработки говнопрайса Билайн\n"
            "Выберите файл .xls для обработки\n"
        )
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setMinimumHeight(100)
        main_layout.addWidget(self.label)

        self.file_display = QLabel(
            "После выбора файла и нажатия кнопки 'Обработать', дождитесь надписи 'Готово...'"
        )
        self.file_display.setAlignment(Qt.AlignCenter)
        self.file_display.setWordWrap(True)
        self.file_display.setMinimumHeight(50)
        main_layout.addWidget(self.file_display)

        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)

        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setPlaceholderText(
            "Пример данных из файла прайса:\n"
            "DEST | COUNTRY CODE | ROLLUP | RATE | COMMENTS | EFFECTIVED\n"
            "Австралия (fix) - Satellite&Premium | 61 | 13-14, 190 | 2,5824 | No Change | 01 Октябрь 2024 г.\n"
            "Адыгея Майкоп (fix) | 7 | 8772 | 0,9999 | No Change | 01 Октябрь 2024 г.\n"
            "\n"
            "Пример обработанных данных:\n"
            "DEST | COUNTRY CODE | ROLLUP | RATE | MC | CI | FT\n"
            "Австралия (fix) - Satellite&Premium | 61 | 13 | 2.5824 | 1 | 1 | 0\n"
            "Австралия (fix) - Satellite&Premium | 61 | 14 | 2.5824 | 1 | 1 | 0\n"
            "Австралия (fix) - Satellite&Premium | 61 | 190 | 2.5824 | 1 | 1 | 0\n"
            "Адыгея Майкоп (fix) | 7 | 8772 | 0.9999 | 1 | 1 | 0\n"
            )
        main_layout.addWidget(QLabel("Превью:"))
        main_layout.addWidget(self.preview_text, 1)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        main_layout.addLayout(button_layout)

        self.choose_file_button = QPushButton("Выбрать файл")
        self.choose_file_button.clicked.connect(self.choose_file)
        button_layout.addWidget(self.choose_file_button)

        self.process_button = QPushButton("Обработать")
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.process_file)
        button_layout.addWidget(self.process_button)

        self.back_button = QPushButton("Назад")
        button_layout.addWidget(self.back_button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Excel files (*.xlsx, *.xls)")
        if file_path:
            self.input_file = file_path
            self.label.setText(f"Выбранный файл: {self.input_file}")
            self.file_display.setText("")
            self.load_preview()
            self.process_button.setEnabled(True)

    def load_preview(self, max_rows=10):
        try:
            wb = xlrd.open_workbook(self.input_file)
            sheet = wb.sheet_by_index(0)
            preview_lines = []
            for i in range(min(max_rows, sheet.nrows)):
                row = sheet.row_values(i)
                preview_lines.append('\t'.join([str(cell) for cell in row]))
            self.preview_text.setPlainText('\n'.join(preview_lines))
        except Exception as e:
            self.preview_text.setPlainText(f"Ошибка загрузки превью: {str(e)}")

    def process_file(self):
        if not self.input_file or not os.path.isfile(self.input_file):
            self.file_display.setText("Файл не найден. Пожалуйста, выберите файл.")
            return

        self.process_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.thread = BeelineProcessorThread(self.input_file)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.finished.connect(self.on_finished)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def on_finished(self, output_file):
        self.file_display.setText(f"Готово. Файл сохранен как: {output_file}")
        self.process_button.setEnabled(True)
        self.progress_bar.setValue(100)

    def on_error(self, error_message):
        self.file_display.setText(f"Ошибка: {error_message}")
        self.process_button.setEnabled(True)
        self.progress_bar.setValue(0)
