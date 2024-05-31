from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from styles import Styles

class ScriptPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui_elements()

    def create_ui_elements(self):
        main_layout = BoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="20dp"
        )
        self.add_widget(main_layout)

        self.label = MDLabel(
            text="Скрипт еще в разработке",
            font_name=Styles.TEXT_FONT,
            halign="center",
            size_hint_y=None,
            height="40dp"
        )
        main_layout.add_widget(self.label)

        button_layout = BoxLayout(
            orientation="horizontal",
            spacing="20dp",
            size_hint_y=None,
            height="60dp"
        )
        main_layout.add_widget(button_layout)

        self.back_button = MDRaisedButton(
            text="Назад",
            on_press=self.back_button_pressed,
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR
        )
        button_layout.add_widget(self.back_button)

    def back_button_pressed(self, instance):
        self.manager.current = "main"