from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QPlainTextEdit, QApplication
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeySequence

class SummTraffWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scripts = {
            "sms": {
                "title": "SUMMTRAFF SMS",
                "process_function": self.process_data_sms
            },
            "voice": {
                "title": "SUMMTRAFF VOICE",
                "process_function": self.process_data_voice
            }
        }
        self.current_script = "sms"

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # Заголовок
        self.title_label = QLabel(self.scripts[self.current_script]["title"])
        font = self.title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        main_layout.addWidget(self.title_label)

        # Метка "Ввод:"
        self.input_label = QLabel("Ввод:")
        main_layout.addWidget(self.input_label)

        # Поле ввода
        self.input_field = QTextEdit()
        self.input_field.setAcceptRichText(False)
        self.input_field.setPlaceholderText(
            "Вставьте текст для обработки (SMS или VOICE в зависимости от выбранного режима)"
        )
        main_layout.addWidget(self.input_field)

        # Метка "Вывод:"
        self.output_label = QLabel("Вывод:")
        main_layout.addWidget(self.output_label)

        # Поле вывода (read-only)
        self.output_field = QPlainTextEdit()
        self.output_field.setReadOnly(True)
        main_layout.addWidget(self.output_field)

        # Фильтр событий для Ctrl+C
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

        # Переключатели скриптов
        self.sms_button = QPushButton("SMS")
        self.sms_button.clicked.connect(lambda: self.switch_script("sms"))
        button_layout.addWidget(self.sms_button)

        self.voice_button = QPushButton("VOICE")
        self.voice_button.clicked.connect(lambda: self.switch_script("voice"))
        button_layout.addWidget(self.voice_button)

        self.update_script_buttons()

    def eventFilter(self, obj, event):
        # Перехватываем Ctrl+C для нормальной копировки
        if obj == self.output_field and event.type() == QEvent.KeyPress:
            if event.matches(QKeySequence.Copy):
                self.copy_plain_text()
                return True
        return super().eventFilter(obj, event)

    def copy_plain_text(self):
        text = self.output_field.toPlainText()
        QApplication.clipboard().setText(text)

    def update_script_buttons(self):
        self.sms_button.setEnabled(self.current_script != "sms")
        self.voice_button.setEnabled(self.current_script != "voice")

    def switch_script(self, script_name):
        if script_name not in self.scripts:
            return
        self.current_script = script_name
        script_info = self.scripts[script_name]
        self.title_label.setText(script_info["title"])
        self.update_script_buttons()
        self.output_field.clear()

    def process_text(self):
        input_text = self.input_field.toPlainText().strip()
        if not input_text:
            self.output_field.setPlainText("Пожалуйста, введите текст для обработки.")
            return
        output_text = self.scripts[self.current_script]["process_function"](input_text)
        self.output_field.setPlainText(output_text)

    @staticmethod
    def _parse_int(val: str):
        v = val.strip()
        if not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @staticmethod
    def _parse_float(val: str):
        v = val.strip().replace(",", ".")
        if not v:
            return None
        try:
            return float(v)
        except ValueError:
            return None

    @staticmethod
    def _parse_percent(val: str):
        v = val.strip().replace(",", ".").replace("%", "")
        if not v:
            return None
        try:
            return float(v)
        except ValueError:
            return None

    @staticmethod
    def _parse_time_mm_ss(val: str):
        # "8:23" -> секунды, "0:00" -> 0, пустое -> None
        v = val.strip()
        if not v or ":" not in v:
            return None
        try:
            mm, ss = v.split(":")
            return int(mm) * 60 + int(ss)
        except Exception:
            return None

    @staticmethod
    def _format_int_or_none(v):
        return "None" if v is None else str(v)

    @staticmethod
    def _format_float_or_none(v, prec=5):
        return "None" if v is None else f"{v:.{prec}f}"

    @staticmethod
    def _format_time_from_seconds(v):
        if v is None:
            return "None"
        # v — сумма секунд, вернём "mm:ss"
        total = int(v)
        mm = total // 60
        ss = total % 60
        return f"{mm}:{ss:02d}"

    def process_data_sms(self, input_text: str) -> str:
        """
        Суммирование SMS по префиксу (первый столбец до "_").
        Формат гибкий, берём последние значения в строке как:
        Попытки, Успешные попытки, Стоимость вх., Стоимость исх., Маржа.
        Если чего-то нет, ставим None, но имеющиеся поля суммируются.
        """
        lines = [l for l in input_text.splitlines() if l.strip()]
        if not lines:
            return "Нет данных."

        # Пропуск заголовка
        start_index = 0
        header_candidate = lines[0]
        if any(x in header_candidate for x in ("Попытки", "Маржа", "Стоимость")):
            start_index = 1

        # prefix -> агрегаты
        sums = {}

        def ensure_prefix(prefix):
            if prefix not in sums:
                sums[prefix] = {
                    "attempts": None,
                    "success": None,
                    "in_cost": None,
                    "out_cost": None,
                    "margin": None,
                }

        for i in range(start_index, len(lines)):
            line = lines[i]
            parts = line.split()
            if len(parts) < 1:
                continue

            prefix_full = parts[0]
            prefix = prefix_full.split("_")[0]
            ensure_prefix(prefix)
            agg = sums[prefix]

            # берём до 5 последних чисел с конца
            numeric_parts = []
            for p in reversed(parts[1:]):
                iv = self._parse_int(p)
                fv = self._parse_float(p)
                if iv is not None or fv is not None:
                    numeric_parts.append(p)
                if len(numeric_parts) >= 5:
                    break

            while len(numeric_parts) < 5:
                numeric_parts.append("")

            numeric_parts = list(reversed(numeric_parts))

            attempts = self._parse_int(numeric_parts[0])
            success = self._parse_int(numeric_parts[1])
            in_cost = self._parse_float(numeric_parts[2])
            out_cost = self._parse_float(numeric_parts[3])
            margin = self._parse_float(numeric_parts[4])

            if attempts is not None:
                agg["attempts"] = (agg["attempts"] or 0) + attempts
            if success is not None:
                agg["success"] = (agg["success"] or 0) + success
            if in_cost is not None:
                agg["in_cost"] = (agg["in_cost"] or 0.0) + in_cost
            if out_cost is not None:
                agg["out_cost"] = (agg["out_cost"] or 0.0) + out_cost
            if margin is not None:
                agg["margin"] = (agg["margin"] or 0.0) + margin

        header = "Название OP\tПопытки\tУспешные попытки\tСтоимость вх.\tСтоимость исх.\tМаржа"
        output_lines = [header]

        for prefix in sorted(sums.keys()):
            agg = sums[prefix]
            line = (
                f"{prefix}\t"
                f"{self._format_int_or_none(agg['attempts'])}\t"
                f"{self._format_int_or_none(agg['success'])}\t"
                f"{self._format_float_or_none(agg['in_cost'])}\t"
                f"{self._format_float_or_none(agg['out_cost'])}\t"
                f"{self._format_float_or_none(agg['margin'])}"
            )
            output_lines.append(line)

        return "\n".join(output_lines)

    def process_data_voice(self, input_text: str) -> str:
        """
        Суммирование VOICE по префиксу, усреднение ASR/ACD/NER/PDD,
        суммирование остальных числовых полей.
        """
        lines = [l for l in input_text.splitlines() if l.strip()]
        if not lines:
            return "Нет данных."

        # Пропуск заголовка
        start_index = 0
        header_candidate = lines[0]
        if any(x in header_candidate for x in ("ASR", "ACD", "NER", "PDD", "Попытки")):
            start_index = 1

        # prefix -> агрегаты
        sums = {}

        def ensure_prefix(prefix):
            if prefix not in sums:
                sums[prefix] = {
                    "asr_sum": 0.0, "asr_cnt": 0,
                    "acd_sum": 0.0, "acd_cnt": 0,
                    "ner_sum": 0.0, "ner_cnt": 0,
                    "pdd_sum": 0.0, "pdd_cnt": 0,
                    "short_pct_sum": 0.0, "short_pct_cnt": 0,
                    "duration": None,
                    "billed": None,
                    "attempts": None,
                    "hunt_attempts": None,
                    "success": None,
                    "in_cost": None,
                    "out_cost": None,
                    "margin": None,
                }

        for i in range(start_index, len(lines)):
            line = lines[i]
            parts = line.split()
            if len(parts) < 2:
                continue

            prefix_full = parts[0]
            prefix = prefix_full.split("_")[0]
            ensure_prefix(prefix)
            agg = sums[prefix]

            # найдём 6 последних чисел (attempts, hunt_attempts, success, in_cost, out_cost, margin)
            numeric_tail = []
            indices_tail = []
            for idx in range(len(parts) - 1, 0, -1):
                v = parts[idx]
                iv = self._parse_int(v)
                fv = self._parse_float(v)
                if iv is not None or fv is not None:
                    numeric_tail.append(v)
                    indices_tail.append(idx)
                if len(numeric_tail) >= 6:
                    break

            while len(numeric_tail) < 6:
                numeric_tail.insert(0, "")
                indices_tail.insert(0, -1)

            numeric_tail = list(reversed(numeric_tail))
            indices_tail = list(reversed(indices_tail))

            attempts_v = self._parse_int(numeric_tail[0])
            hunt_attempts_v = self._parse_int(numeric_tail[1])
            success_v = self._parse_int(numeric_tail[2])
            in_cost_v = self._parse_float(numeric_tail[3])
            out_cost_v = self._parse_float(numeric_tail[4])
            margin_v = self._parse_float(numeric_tail[5])

            left_end = indices_tail[0]
            left_parts = parts[1:left_end]  # без префикса

            # с конца: billed, duration, short, PDD, NER, ACD, ASR
            def pop_last(lst):
                if not lst:
                    return None
                return lst.pop()

            left = left_parts[:]

            billed_raw = pop_last(left) or ""
            duration_raw = pop_last(left) or ""
            short_raw = pop_last(left) or ""

            pdd_raw = pop_last(left) or ""
            ner_raw = pop_last(left) or ""
            acd_raw = pop_last(left) or ""
            asr_raw = pop_last(left) or ""

            billed_v = self._parse_time_mm_ss(billed_raw)
            duration_v = self._parse_time_mm_ss(duration_raw)
            short_calls_v = self._parse_percent(short_raw)

            pdd_v = self._parse_float(pdd_raw)  # часто время, просто float
            ner_v = self._parse_percent(ner_raw)
            acd_v = self._parse_time_mm_ss(acd_raw)  # ACD — длительность
            asr_v = self._parse_percent(asr_raw)

            # Средние
            if asr_v is not None:
                agg["asr_sum"] += asr_v
                agg["asr_cnt"] += 1
            if acd_v is not None:
                agg["acd_sum"] += acd_v
                agg["acd_cnt"] += 1
            if ner_v is not None:
                agg["ner_sum"] += ner_v
                agg["ner_cnt"] += 1
            if pdd_v is not None:
                agg["pdd_sum"] += pdd_v
                agg["pdd_cnt"] += 1

            # Суммируемые
            if short_calls_v is not None:
                agg["short_pct_sum"] += short_calls_v
                agg["short_pct_cnt"] += 1
            if duration_v is not None:
                agg["duration"] = (agg["duration"] or 0) + duration_v
            if billed_v is not None:
                agg["billed"] = (agg["billed"] or 0) + billed_v

            if attempts_v is not None:
                agg["attempts"] = (agg["attempts"] or 0) + attempts_v
            if hunt_attempts_v is not None:
                agg["hunt_attempts"] = (agg["hunt_attempts"] or 0) + hunt_attempts_v
            if success_v is not None:
                agg["success"] = (agg["success"] or 0) + success_v

            if in_cost_v is not None:
                agg["in_cost"] = (agg["in_cost"] or 0.0) + in_cost_v
            if out_cost_v is not None:
                agg["out_cost"] = (agg["out_cost"] or 0.0) + out_cost_v
            if margin_v is not None:
                agg["margin"] = (agg["margin"] or 0.0) + margin_v

        header = (
            "Название OP\tASR\tACD\tNER\tPDD\tКороткие звонки\tДлительность\t"
            "Тарифицировано\tПопытки\tПопытки хантинга\tУспешные попытки\t"
            "Стоимость вх.\tСтоимость исх.\tМаржа"
        )
        output_lines = [header]

        for prefix in sorted(sums.keys()):
            agg = sums[prefix]

            asr_avg = agg["asr_sum"] / agg["asr_cnt"] if agg["asr_cnt"] > 0 else None
            acd_avg_sec = agg["acd_sum"] / agg["acd_cnt"] if agg["acd_cnt"] > 0 else None
            ner_avg = agg["ner_sum"] / agg["ner_cnt"] if agg["ner_cnt"] > 0 else None
            pdd_avg = agg["pdd_sum"] / agg["pdd_cnt"] if agg["pdd_cnt"] > 0 else None
            short_pct_avg = (agg["short_pct_sum"] / agg["short_pct_cnt"] if agg["short_pct_cnt"] > 0 else None)

            line = (
                f"{prefix}\t"
                f"{self._format_float_or_none(asr_avg, 2)}%\t"
                f"{self._format_time_from_seconds(acd_avg_sec)}\t"
                f"{self._format_float_or_none(ner_avg, 2)}%\t"
                f"{self._format_float_or_none(pdd_avg, 2)}\t"
                f"{self._format_float_or_none(short_pct_avg, 2)}%\t"
                f"{self._format_time_from_seconds(agg['duration'])}\t"
                f"{self._format_time_from_seconds(agg['billed'])}\t"
                f"{self._format_int_or_none(agg['attempts'])}\t"
                f"{self._format_int_or_none(agg['hunt_attempts'])}\t"
                f"{self._format_int_or_none(agg['success'])}\t"
                f"{self._format_float_or_none(agg['in_cost'])}\t"
                f"{self._format_float_or_none(agg['out_cost'])}\t"
                f"{self._format_float_or_none(agg['margin'])}"
            )
            output_lines.append(line)

        return "\n".join(output_lines)
