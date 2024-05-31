from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from styles import Styles

class PrefixPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui_elements()
        self.scripts = {
            "prefiltr": {
                "title": "PREFILTR",
                "process_function": self.prefiltr
            },
            "prefdel": {
                "title": "PREFDEL",
                "process_function": self.prefdel
            }
        }
        self.current_script = "prefiltr"

    def prefiltr(self, input_text, prefix):
        values = [int(value) for value in input_text.splitlines() if value.strip()]
        original_count = len(values)
        filtered_values = [value for value in values if any(str(value).startswith(prefix) for prefix in [prefix])]
        filtered_count = len(filtered_values)
        removed_count = original_count - filtered_count
        output_text = "\n".join(map(str, filtered_values))
        output_text += f"\n\nКоличество не попавших под фильтр строк: {removed_count}"
        output_text += f"\nКоличество отфильтрованных строк с указанным префиксом: {filtered_count}"
        return output_text

    def prefdel(self, input_text, prefix):
        lines = input_text.splitlines()
        original_count = len(lines)
        filtered_lines = [line for line in lines if not line.startswith(prefix)]
        removed_count = original_count - len(filtered_lines)
        output_text = "\n".join(filtered_lines)
        output_text += f"\n\nКоличество оставшихся строк: {len(filtered_lines)}"
        output_text += f"\nКоличество удаленных строк с указанным префиксом: {removed_count}"
        return output_text

    def create_ui_elements(self):
        main_layout = BoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="20dp"
        )
        self.add_widget(main_layout)

        self.title_label = MDLabel(
            text="PREFILTR",
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

        self.prefix_label = MDLabel(
            text="Префикс:",
            font_name=Styles.TEXT_FONT,
            halign="left",
            size_hint_y=None,
            height="40dp"
        )
        main_layout.add_widget(self.prefix_label)

        self.prefix_field = MDTextField(
            hint_text="Введите префикс",
            font_name=Styles.ENTRY_FONT,
            size_hint=(1, None),
            height="40dp"
        )
        main_layout.add_widget(self.prefix_field)

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

        self.prefiltr_button = MDRaisedButton(
            text="PREFILTR",
            on_press=lambda x: self.switch_script("prefiltr"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1}
        )
        button_layout.add_widget(self.prefiltr_button)

        self.prefdel_button = MDRaisedButton(
            text="PREFDEL",
            on_press=lambda x: self.switch_script("prefdel"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1}
        )
        button_layout.add_widget(self.prefdel_button)

    def process_text(self, instance):
        input_text = self.input_field.text
        prefix = self.prefix_field.text
        output_text = self.scripts[self.current_script]["process_function"](input_text, prefix)
        self.output_field.text = output_text

    def switch_script(self, script_name):
        self.current_script = script_name
        script_info = self.scripts[script_name]
        self.title_label.text = script_info["title"]
        self.scripts[script_name]["process_function"] = getattr(self, f"{script_name}")

    def back_button_pressed(self, instance):
        self.manager.current = "main"