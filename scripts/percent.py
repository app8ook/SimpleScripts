from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QPlainTextEdit, QApplication
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeySequence


class PercentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.modes = {
            "plus": {
                "title": "N + %",
                "op": self._calc_plus
            },
            "minus": {
                "title": "N - %",
                "op": self._calc_minus
            }
        }
        self.current_mode = "plus"

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # Заголовок
        self.title_label = QLabel(self.modes[self.current_mode]["title"])
        font = self.title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        main_layout.addWidget(self.title_label)

        # Поле значений
        self.values_label = QLabel("Значения:")
        main_layout.addWidget(self.values_label)

        self.values_edit = QTextEdit()
        self.values_edit.setPlaceholderText("Каждое значение с новой строки (например: 5.222)")
        self.values_edit.setAcceptRichText(False)
        main_layout.addWidget(self.values_edit)

        # Поле процентов
        self.percents_label = QLabel("Проценты:")
        main_layout.addWidget(self.percents_label)

        self.percents_edit = QTextEdit()
        self.percents_edit.setAcceptRichText(False)
        self.percents_edit.setPlaceholderText(
            "Каждый процент с новой строки.\n"
            "Варианты:\n"
            "- столько же строк, сколько значений\n"
            "- одна строка (один процент на все значения)"
        )
        self.percents_edit.setAcceptRichText(False)
        main_layout.addWidget(self.percents_edit)

        # Вывод
        self.output_label = QLabel("Результат:")
        main_layout.addWidget(self.output_label)

        self.output_field = QPlainTextEdit()
        self.output_field.setReadOnly(True)
        main_layout.addWidget(self.output_field)
        self.output_field.installEventFilter(self)

        main_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Кнопки
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

        self.plus_button = QPushButton("N + %")
        self.plus_button.clicked.connect(lambda: self.switch_mode("plus"))
        button_layout.addWidget(self.plus_button)

        self.minus_button = QPushButton("N - %")
        self.minus_button.clicked.connect(lambda: self.switch_mode("minus"))
        button_layout.addWidget(self.minus_button)

        self.update_mode_buttons()

    def eventFilter(self, obj, event):
        # Копирование результата
        if obj == self.output_field and event.type() == QEvent.KeyPress:
            if event.matches(QKeySequence.Copy):
                text = self.output_field.toPlainText()
                QApplication.clipboard().setText(text)
                return True
        return super().eventFilter(obj, event)

    def update_mode_buttons(self):
        self.plus_button.setEnabled(self.current_mode != "plus")
        self.minus_button.setEnabled(self.current_mode != "minus")

    def switch_mode(self, mode_name):
        if mode_name not in self.modes:
            return
        self.current_mode = mode_name
        self.title_label.setText(self.modes[mode_name]["title"])
        self.update_mode_buttons()
        self.output_field.clear()

    @staticmethod
    def _parse_float_line(s: str):
        s = s.strip().replace(",", ".")
        if not s:
            return None
        try:
            return float(s)
        except ValueError:
            return None

    @staticmethod
    def _calc_plus(value: float, percent: float) -> float:
        return value * (1.0 + percent / 100.0)

    @staticmethod
    def _calc_minus(value: float, percent: float) -> float:
        return value * (1.0 - percent / 100.0)


    def process_text(self):
        values_raw = self.values_edit.toPlainText().splitlines()
        percents_raw = self.percents_edit.toPlainText().splitlines()

        values = [self._parse_float_line(x) for x in values_raw]
        percents = [self._parse_float_line(x) for x in percents_raw]

        # Фильтруем пустые строки (None) по обеим колонкам независимо
        values = [v for v in values if v is not None]
        percents = [p for p in percents if p is not None]

        if not values:
            self.output_field.setPlainText("Ошибка: нет значений для расчёта.")
            return
        if not percents:
            self.output_field.setPlainText("Ошибка: нет процентов для расчёта.")
            return

        n_vals = len(values)
        n_pcts = len(percents)

        if n_vals == n_pcts:
            percent_list = percents
        elif n_vals > 1 and n_pcts == 1:
            percent_list = [percents[0]] * n_vals
        else:
            self.output_field.setPlainText(
                "Ошибка: количество строк значений и процентов не совпадает.\n"
                "Допустимо:\n"
                "- одинаковое количество строк\n"
                "- несколько значений и один процент."
            )
            return

        op_func = self.modes[self.current_mode]["op"]
        lines_out = []
        for v, p in zip(values, percent_list):
            try:
                res = op_func(v, p)
                lines_out.append(f"{res:.6f}")
            except Exception as e:
                lines_out.append(f"Ошибка вычисления: {e}")

        self.output_field.setPlainText("\n".join(lines_out))