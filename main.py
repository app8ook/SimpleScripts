from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from pages.base import BasePage
from styles import apply_styles
from kivy.core.window import Window
import os

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.icon = os.path.join(os.path.dirname(__file__), "Kosou.png")
        self.title = "Simple Scripts 0.1"

    def build(self):
        # Установка размера окна
        Window.size = (900, 900)  # Ширина и высота окна в пикселях
        Window.minimum_size = (640, 480)  # Минимальный размер окна

        # Центрирование окна на экране
        Window.left = (Window.width - 800) // 2
        Window.top = (Window.height - 600) // 2
        if os.name == 'nt':  # Windows
            Window.left = 100
            Window.top = 100
        else:  # Другие ОС
            Window.position = (100, 100)
        
        Window.icon = os.path.join(os.path.dirname(__file__), "Kosou.png")
        self.screen_manager = ScreenManager()
        self.apply_styles()
        self.main_page = BasePage(name="main")
        self.screen_manager.add_widget(self.main_page)
        self.load_pages()

        return self.screen_manager

    def load_pages(self):
        from pages.duplicate import DuplicatePage
        from pages.prefix import PrefixPage
        from pages.aster import AsterPage
        from pages.num import NumPage
        from pages.mysql import MysqlPage
        from pages.script import ScriptPage
        from pages.kosou import KosouPage
        self.screen_manager.add_widget(DuplicatePage(name="duplicates"))
        self.screen_manager.add_widget(PrefixPage(name="prefix"))
        self.screen_manager.add_widget(AsterPage(name="aster"))
        self.screen_manager.add_widget(NumPage(name="num"))
        self.screen_manager.add_widget(MysqlPage(name="mysql"))
        self.screen_manager.add_widget(ScriptPage(name="script"))
        self.screen_manager.add_widget(KosouPage(name="kosou"))

    def apply_styles(self):
        apply_styles(self)

if __name__ == "__main__":
    MainApp().run()