from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from styles import Styles

class BasePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_main_page_buttons()

    def create_main_page_buttons(self):
        main_layout = FloatLayout()
        self.add_widget(main_layout)

        button_container = BoxLayout(
            orientation="vertical",
            spacing="20dp",
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.8, 'center_y': 0.7},
        )
        main_layout.add_widget(button_container)

        self.create_button("Удаление дубликатов", "duplicates", button_container)
        self.create_button("Фильтрация 2 пачек данных", "dbldata", button_container)
        self.create_button("Удаление и фильтрация по префиксам", "prefix", button_container)
        self.create_button("Настройка номеров для Aster", "aster", button_container)
        self.create_button("Форматирование списаний по номерам", "num", button_container)
        self.create_button("Скрипты для запросов в MYSQL", "mysql", button_container)
        self.create_button("Переработка прайсов Би", "gprices", button_container)
        self.create_button("Скрипт в разработке", "script", button_container)
        self.create_button("Об авторе", "kosou", button_container)

    def create_button(self, text, page_name, parent):
        button = MDRaisedButton(
            text=text,
            on_press=lambda _: self.switch_page(page_name),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR
        )
        parent.add_widget(button)

    def switch_page(self, page_name):
        self.manager.current = page_name