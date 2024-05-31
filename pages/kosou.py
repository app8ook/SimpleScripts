from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from styles import Styles
import webbrowser

class KosouPage(Screen):
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

        button_container = BoxLayout(
            orientation="vertical",
            spacing="20dp",
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.8, 'center_y': 0.9},
            padding=[0, 0, 0, "300dp"]
        )
        main_layout.add_widget(button_container)

        self.create_button("Сайт автора", "sitelink", button_container)
        self.create_button("Вопросы и предложения по программе", "telegramlink", button_container)

        button_layout = BoxLayout(
            orientation="horizontal",
            spacing="20dp",
            size_hint_y=None,
            height="60dp",
            padding=[0, 0, 0, "5dp"]
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

    def create_button(self, text, page_name, parent):
        button = MDRaisedButton(
            text=text,
            on_press=lambda _: self.open_link(page_name),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR
        )
        parent.add_widget(button)

    def open_link(self, page_name):
        if page_name == "sitelink":
            # Замените на ваш веб-сайт
            webbrowser.open("https://app8ook.github.io")
        elif page_name == "telegramlink":
            # Замените на ваш Telegram профиль
            webbrowser.open("https://t.me/blobx")

    def back_button_pressed(self, instance):
        self.manager.current = "main"