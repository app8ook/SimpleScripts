from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from styles import Styles

class DbldataPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui_elements()
        self.scripts = {
            "filtrdata": {
                "title": "FILTRDATA",
                "process_function": self.filtrdata_data
            },
            "deldata": {
                "title": "DELDATA",
                "process_function": self.deldata_data
            }
        }
        self.current_script = "filtrdata"

    def create_ui_elements(self):
        main_layout = BoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="20dp"
        )
        self.add_widget(main_layout)

        self.title_label = MDLabel(
            text="FILTRDATA",
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

        self.input_label2 = MDLabel(
            text="Фильтр:",
            font_name=Styles.TEXT_FONT,
            halign="left",
            size_hint_y=None,
            height="40dp"
        )
        main_layout.add_widget(self.input_label2)

        self.input_field2 = TextInput(
            hint_text="Введите фильтр",
            font_name=Styles.ENTRY_FONT,
            size_hint=(1, 0.4),
            multiline=True
        )
        main_layout.add_widget(self.input_field2)

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

        self.filtrdata_button = MDRaisedButton(
            text="FILTRDATA",
            on_press=lambda x: self.switch_script("filtrdata"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1}
        )
        button_layout.add_widget(self.filtrdata_button)

        self.deldata_button = MDRaisedButton(
            text="DELDATA",
            on_press=lambda x: self.switch_script("deldata"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1}
        )
        button_layout.add_widget(self.deldata_button)

    def filtrdata_data(self, input_text):
        try:
            input_elements = [element.strip() for line in input_text.split('\n') for element in line.split()]
            filter_elements = [element.strip() for element in self.input_field2.text.split()]

            filtered_elements = [element for element in input_elements if element in filter_elements]
            filtered_lines = [' '.join(line.split()) for line in input_text.split('\n') if any(element in line for element in filtered_elements)]
            return '\n'.join(filtered_lines)
        except Exception as e:
            output_lines.append(f"Ошибка в строке {i}: {str(e)}")

    def deldata_data(self, input_text):
        try:
            input_elements = [element.strip() for line in input_text.split('\n') for element in line.split()]
            filter_elements = [element.strip() for element in self.input_field2.text.split()]

            deleted_elements = [element for element in input_elements if element not in filter_elements]
            deleted_lines = [' '.join(line.split()) for line in input_text.split('\n') if all(element not in line for element in filter_elements)]
            return '\n'.join(deleted_lines)
        except Exception as e:
            output_lines.append(f"Ошибка в строке {i}: {str(e)}")

    def switch_script(self, script_name):
        self.current_script = script_name
        script_info = self.scripts[script_name]
        self.title_label.text = script_info["title"]
        self.scripts[script_name]["process_function"] = getattr(self, f"{script_name}_data")

    def process_text(self, instance):
        input_text = self.input_field.text.strip()
        if not input_text:
            return
        output_text = self.scripts[self.current_script]["process_function"](input_text)
        self.output_field.text = output_text

    def back_button_pressed(self, instance):
        self.manager.current = "main"