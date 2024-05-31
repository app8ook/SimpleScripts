from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from styles import Styles

class AsterPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui_elements()
        self.scripts = {
            "inc": {
                "title": "INC",
                "prefix_label": "Префикс:",
                "prefix_hint": "Введите префикс",
                "comment_label": "Комментарий:",
                "comment_hint": "Введите комментарий",
                "generate_function": self.generate_inc_dialplan
            },
            "noinc": {
                "title": "NOINC",
                "prefix_label": "",
                "prefix_hint": "",
                "comment_label": "Комментарий:",
                "comment_hint": "Введите комментарий",
                "generate_function": self.generate_noinc_dialplan
            }
        }
        self.current_script = "inc"

    def create_ui_elements(self):
        main_layout = BoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="20dp"
        )
        self.add_widget(main_layout)

        self.title_label = MDLabel(
            text="IVR",
            halign="left",
            size_hint_y=None,
            height="30dp"
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

        self.comment_label = MDLabel(
            text="Комментарий:",
            font_name=Styles.TEXT_FONT,
            halign="left",
            size_hint_y=None,
            height="40dp"
        )
        main_layout.add_widget(self.comment_label)

        self.comment_field = MDTextField(
            hint_text="Введите комментарий",
            font_name=Styles.ENTRY_FONT,
            size_hint=(1, None),
            height="40dp"
        )
        main_layout.add_widget(self.comment_field)

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

        self.generate_button = MDRaisedButton(
            text="Сгенерировать",
            on_press=self.generate_dialplan,
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR
        )
        button_layout.add_widget(self.generate_button)

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

        self.inc_button = MDRaisedButton(
            text="INC",
            on_press=lambda x: self.switch_script("inc"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1}
        )
        button_layout.add_widget(self.inc_button)

        self.ivr_button = MDRaisedButton(
            text="NOINC",
            on_press=lambda x: self.switch_script("noinc"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1}
        )
        button_layout.add_widget(self.ivr_button)

    def generate_inc_dialplan(self, instance):
        numbers = self.input_field.text.strip().splitlines()
        prefix = self.prefix_field.text
        comment = self.comment_field.text
        output = self.generate_inc_dialplan_entries(numbers, prefix, comment)
        self.output_field.text = output

    def generate_noinc_dialplan(self, instance):
        numbers = self.input_field.text.strip().splitlines()
        comment = self.comment_field.text
        output = self.generate_noinc_dialplan_entries(numbers, comment)
        self.output_field.text = output

    def generate_inc_dialplan_entries(self, numbers, prefix, comment):
        dialplan_entries = []
        processed_count = 0
        for number in numbers:
            entry = f"exten => {number},1,Log(NOTICE, Incoming for {comment})\n" \
                    f" same => n,Dial(SIP/mediacore/{prefix}${number},60)\n" \
                    f" same => n,Hangup()"
            dialplan_entries.append(entry)
            processed_count += 1
        output = "\n\n".join(dialplan_entries)
        output += f"\n\nУспешно обработано номеров: {processed_count}"
        return output

    def generate_noinc_dialplan_entries(self, numbers, comment):
        dialplan_entries = []
        processed_count = 0
        for number in numbers:
            entry = f"exten => {number},1,Log(NOTICE, incoming for {comment})\n" \
                    " same => n,Answer()\n" \
                    " same => n,Wait(1)\n" \
                    " same => n,Playback(/var/lib/asterisk/sounds/lv/IVR,skip)\n" \
                    " same => n,Hangup()"
            dialplan_entries.append(entry)
            processed_count += 1
        output = "\n\n".join(dialplan_entries)
        output += f"\n\nУспешно обработано номеров: {processed_count}"
        return output

    def switch_script(self, script_name):
        self.current_script = script_name
        script_info = self.scripts[script_name]
        self.prefix_label.text = script_info["prefix_label"]
        self.prefix_field.hint_text = script_info["prefix_hint"]
        self.comment_label.text = script_info["comment_label"]
        self.comment_field.hint_text = script_info["comment_hint"]
        self.title_label.text = script_info["title"]
        self.scripts[script_name]["generate_function"] = getattr(self, f"generate_{script_name}_dialplan")

    def generate_dialplan(self, instance):
        input_text = self.input_field.text.strip()
        if not input_text:
            return
        self.scripts[self.current_script]["generate_function"](instance)

    def back_button_pressed(self, instance):
        self.manager.current = "main"