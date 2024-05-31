from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from styles import Styles

class DuplicatePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui_elements()

#Сам скрипт
    def remove_duplicates_and_count(self, input_text):
        lines = input_text.splitlines()
        unique_lines = list(set(lines))
        removed_count = len(lines) - len(unique_lines)
        output_text = "\n".join(unique_lines)
        output_text += f"\n\nКоличество уникальных строк: {len(unique_lines)}"
        output_text += f"\nКоличество удаленных дубликатов: {removed_count}"
        return output_text

#Создание элементов на странице
    def create_ui_elements(self):
        main_layout = BoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="20dp"
        )
        self.add_widget(main_layout)

#Поле ввода
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

#Поле вывода
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

#Кнопка обработать
        self.process_button = MDRaisedButton(
            text="Обработать",
            on_press=self.process_text,
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR
        )
        button_layout.add_widget(self.process_button)

#Кнопка назад
        self.back_button = MDRaisedButton(
            text="Назад",
            on_press=self.back_button_pressed,
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR
        )
        button_layout.add_widget(self.back_button)

#Подвязка скрипта к текстовым полям и кнопкам
    def process_text(self, instance):
        input_text = self.input_field.text
        output_text = self.remove_duplicates_and_count(input_text)
        self.output_field.text = output_text

    def back_button_pressed(self, instance):
        self.manager.current = "main"