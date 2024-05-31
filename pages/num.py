from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from styles import Styles

class NumPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui_elements()
        self.scripts = {
            "numbd": {
                "title": "NUMBD",
                "process_function": self.process_data_numbd
            },
            "numadmn": {
                "title": "NUMADMN",
                "process_function": self.process_data_numadmn
            }
        }
        self.current_script = "numbd"

    def create_ui_elements(self):
        main_layout = BoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="20dp"
        )
        self.add_widget(main_layout)

        self.title_label = MDLabel(
            text="NUMBD",
            font_name=Styles.TEXT_FONT,
            halign="left",
            size_hint_y=None,
            height="40dp"
        )
        main_layout.add_widget(self.title_label)

        self.input_label = MDLabel(
            text="Ввод:",
            font_name=Styles.TEXT_FONT,
            halign="left",
            size_hint_y=None,
            height="40dp"
        )
        main_layout.add_widget(self.input_label)

        self.input_field = TextInput(
            hint_text="Введите текст",
            font_name=Styles.ENTRY_FONT,
            size_hint=(1, 0.4),
            multiline=True
        )
        main_layout.add_widget(self.input_field)

        self.output_label = MDLabel(
            text="Вывод:",
            font_name=Styles.TEXT_FONT,
            halign="left",
            size_hint_y=None,
            height="40dp"
        )
        main_layout.add_widget(self.output_label)

        self.output_field = TextInput(
            hint_text="Результат",
            font_name=Styles.ENTRY_FONT,
            size_hint=(1, 0.4),
            multiline=True,
            readonly=True
        )
        main_layout.add_widget(self.output_field)

        button_layout = BoxLayout(
            orientation="horizontal",
            spacing="20dp",
            size_hint_y=None,
            height="60dp"
        )
        main_layout.add_widget(button_layout)

        self.process_button = MDRaisedButton(
            text="Обработать",
            on_press=self.process_text,
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR
        )
        button_layout.add_widget(self.process_button)

        self.back_button = MDRaisedButton(
            text="Назад",
            on_press=self.back_button_pressed,
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR
        )
        button_layout.add_widget(self.back_button)

        button_layout.add_widget(Widget(size_hint_x=0.1))

        self.numbd_button = MDRaisedButton(
            text="NUMBD",
            on_press=lambda x: self.switch_script("numbd"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1}
        )
        button_layout.add_widget(self.numbd_button)

        self.numadmn_button = MDRaisedButton(
            text="NUMADMN",
            on_press=lambda x: self.switch_script("numadmn"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1}
        )
        button_layout.add_widget(self.numadmn_button)

    def process_data_numbd(self, input_text):
        # Разделяем входные данные на строки
        lines = input_text.splitlines()
        
        # Обрабатываем заголовок
        header = lines[0].replace(",", "\t")
        header = "Дата\tЦена\tНомер\tОписание"
        
        # Обрабатываем остальные строки
        output_lines = []
        for line in lines[1:]:
            # Пропускаем строки с "Balance refill" и "Phone number verification"
            if "Balance refill" in line or "Phone number verification" in line:
                continue
            
            # Разделяем строку на части
            parts = line.split(",")
            
            # Обрабатываем дату
            date = parts[0].strip('"')
            
            # Обрабатываем цену
            price = parts[2].replace("-", "").replace(".", ",")
            
            # Обрабатываем номер и описание
            if "Monthly charge for renting a phone number" in parts[4]:
                number = parts[4].split("'")[1]
                description = "Абонентская плата"
            elif "Connection cost for a phone number" in parts[4]:
                number = parts[4].split("'")[1]
                description = "Плата за подключение"
            else:
                number = parts[4].split("'")[1] if "'" in parts[4] else ""
                description = parts[4].replace("'", "")
            
            # Формируем выходную строку
            output_line = f"{date}\t{price}\t{number}\t{description}"
            output_lines.append(output_line)
        
        # Формируем выходной текст
        output_text = "\n".join([header] + output_lines)
        return output_text

    def process_data_numadmn(self, input_text):
        # Разделяем входные данные на строки
        lines = input_text.splitlines()
        
        # Обрабатываем заголовок
        header = lines[0].replace(",", "\t")
        header = "Дата\tЦена\tНомер\tОписание"
        
        # Обрабатываем остальные строки
        output_lines = []
        for line in lines[1:]:
            # Пропускаем строки с "Пополнение", "Верификация", "тикет", "Счет"
            if "Пополнение" in line or "Верификация" in line or "тикет" in line or "Счет" in line:
                continue
            
            # Разделяем строку на части
            parts = line.split("\t")
            
            # Обрабатываем дату
            date = parts[0].replace(",", ".")
            
            # Обрабатываем цену, номер и описание
            if "Ежемесячное списание за использование номера" in parts[2]:
                number = parts[2].split(" ")[-1]
                description = "Абонентская плата"
                price = parts[1].replace("-", "").replace(".", ",")
            elif "A number margin: Списание за А-номер:" in parts[2]:
                number = parts[2].split(": ")[-1]
                description = "Абонентская плата"
                price = parts[3].replace("-", "").replace(".", ",")
            elif "Payment for A number" in parts[2]:
                number = parts[2].split(" ")[-1]
                description = "Плата за подключение"
                price = parts[3].replace("-", "").replace(".", ",")
            elif "Списание за подключение номера" in parts[2]:
                number = parts[2].split(" ")[-1]
                description = "Плата за подключение"
                price = parts[1].replace("-", "").replace(".", ",")
            elif "HLR" in parts[2]:
                number = ""
                description = "HLR"
                price = parts[1].replace("-", "").replace(".", ",")
            else:
                number = parts[2]
                description = parts[2]
                price = parts[1].replace("-", "").replace(".", ",")
            
            # Формируем выходную строку
            output_line = f"{date}\t{price}\t{number}\t{description}"
            output_lines.append(output_line)
        
        # Формируем выходной текст
        output_text = "\n".join([header] + output_lines)
        
        return output_text

    def switch_script(self, script_name):
        self.current_script = script_name
        script_info = self.scripts[script_name]
        self.title_label.text = script_info["title"]
        self.scripts[script_name]["process_function"] = getattr(self, f"process_data_{script_name}")

#Подвязка скрипта к текстовым полям и кнопкам
    def process_text(self, instance):
        input_text = self.input_field.text.strip()
        if not input_text:
            return
        output_text = self.scripts[self.current_script]["process_function"](input_text)
        self.output_field.text = output_text

    def back_button_pressed(self, instance):
        self.manager.current = "main"