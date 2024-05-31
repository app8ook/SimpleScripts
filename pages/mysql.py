from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from styles import Styles

class MysqlPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui_elements()
        self.scripts = {
            "ivr": {
                "title": "IVR",
                "context_label": "Контекст:",
                "context_hint": "Введите контекст",
                "client_label": "Клиент:",
                "client_hint": "Введите ID",
                "prefix_label": "",
                "prefix_hint": "",
                "ivr_label": "Путь к IVR:",
                "ivr_hint": "Введите путь к IVR"
            },
            "ivr_to_inc": {
                "title": "IVRTOINC",
                "context_label": "Контекст:",
                "context_hint": "Введите контекст",
                "client_label": "Клиент:",
                "client_hint": "Введите ID",
                "prefix_label": "Префикс:",
                "prefix_hint": "Введите префикс",
                "ivr_label": "",
                "ivr_hint": ""
            },
            "ivr_lv": {
                "title": "IVRLV",
                "context_label": "Контекст:",
                "context_hint": "Введите контекст",
                "client_label": "Клиент:",
                "client_hint": "Введите ID",
                "prefix_label": "",
                "prefix_hint": "",
                "ivr_label": "",
                "ivr_hint": ""
            },
            "inc": {
                "title": "INC",
                "context_label": "Контекст:",
                "context_hint": "Введите контекст",
                "client_label": "Клиент:",
                "client_hint": "Введите ID",
                "prefix_label": "Префикс:",
                "prefix_hint": "Введите префикс",
                "ivr_label": "",
                "ivr_hint": ""
            },
            "inc_to_ivr": {
                "title": "INCTOIVR",
                "context_label": "Контекст:",
                "context_hint": "Введите контекст",
                "client_label": "Клиент:",
                "client_hint": "Введите ID",
                "prefix_label": "",
                "prefix_hint": "",
                "ivr_label": "Путь к IVR:",
                "ivr_hint": "Введите путь к IVR"
            },
            "del": {
                "title": "DEL",
                "context_label": "",
                "context_hint": "",
                "client_label": "",
                "client_hint": "",
                "prefix_label": "",
                "prefix_hint": "",
                "ivr_label": "",
                "ivr_hint": ""
            }
            # Добавьте другие скрипты здесь
        }
        self.current_script = "ivr"

    def create_ui_elements(self):
        main_layout = BoxLayout(
            orientation="vertical",
            padding="10dp",
            spacing="10dp"
        )
        self.add_widget(main_layout)

        # Заголовок
        self.title_label = MDLabel(
            text="IVR",
            halign="left",
            size_hint_y=None,
            height="30dp"
        )
        main_layout.add_widget(self.title_label)

        # Поле ввода номеров
        self.numbers_label = MDLabel(
            text="Номера:",
            font_name=Styles.TEXT_FONT,
            halign="left",
            size_hint_y=None,
            height="30dp",
            padding=[0, 5, 0, 5]
        )
        main_layout.add_widget(self.numbers_label)

        self.numbers_field = TextInput(
            hint_text="Введите номера через новую строку",
            font_name=Styles.ENTRY_FONT,
            size_hint=(1, 0.3),
            multiline=True,
            padding="5dp"
        )
        main_layout.add_widget(self.numbers_field)

        # Поле ввода контекста
        self.context_label = MDLabel(
            text="Контекст:",
            font_name=Styles.TEXT_FONT,
            halign="left",
            size_hint_y=None,
            height="30dp",
            padding=[0, 5, 0, 5]
        )
        main_layout.add_widget(self.context_label)

        self.context_field = MDTextField(
            hint_text="Введите контекст",
            font_name=Styles.ENTRY_FONT,
            size_hint=(1, None),
            height="30dp",
            padding="5dp"
        )
        main_layout.add_widget(self.context_field)

        # Поле ввода клиента
        self.client_label = MDLabel(
            text="Клиент:",
            font_name=Styles.TEXT_FONT,
            halign="left",
            size_hint_y=None,
            height="30dp",
            padding=[0, 5, 0, 5]
        )
        main_layout.add_widget(self.client_label)

        self.client_field = MDTextField(
            hint_text="Введите клиента",
            font_name=Styles.ENTRY_FONT,
            size_hint=(1, None),
            height="30dp",
            padding="5dp"
        )
        main_layout.add_widget(self.client_field)

        # Поле ввода пути к IVR
        self.ivr_label = MDLabel(
            text="Путь к IVR:",
            font_name=Styles.TEXT_FONT,
            halign="left",
            size_hint_y=None,
            height="30dp",
            padding=[0, 5, 0, 5]
        )
        main_layout.add_widget(self.ivr_label)

        self.ivr_field = MDTextField(
            hint_text="Введите путь к IVR",
            font_name=Styles.ENTRY_FONT,
            size_hint=(1, None),
            height="30dp",
            padding="5dp"
        )
        main_layout.add_widget(self.ivr_field)

        # Поле ввода префикса
        self.prefix_label = MDLabel(
            text="Префикс:",
            font_name=Styles.TEXT_FONT,
            halign="left",
            size_hint_y=None,
            height="30dp",
            padding=[0, 5, 0, 5]
        )
        main_layout.add_widget(self.prefix_label)

        self.prefix_field = MDTextField(
            hint_text="Введите префикс",
            font_name=Styles.ENTRY_FONT,
            size_hint=(1, None),
            height="30dp",
            padding="5dp"
        )
        main_layout.add_widget(self.prefix_field)

        # Поле вывода
        self.output_label = MDLabel(
            text="Вывод:",
            font_name=Styles.TEXT_FONT,
            halign="left",
            size_hint_y=None,
            height="30dp",
            padding=[0, 5, 0, 5]
        )
        main_layout.add_widget(self.output_label)

        self.output_field = TextInput(
            hint_text="Результат",
            font_name=Styles.ENTRY_FONT,
            size_hint=(1, 0.3),
            multiline=True,
            readonly=True,
            padding="5dp"
        )
        main_layout.add_widget(self.output_field)

        button_layout = BoxLayout(
            orientation="horizontal",
            spacing="10dp",
            size_hint_y=None,
            height="50dp"
        )
        main_layout.add_widget(button_layout)

        # Кнопка "Сгенерировать запрос"
        self.generate_button = MDRaisedButton(
            text="Сгенерировать запрос",
            on_press=self.generate_query,
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            padding="5dp"
        )
        button_layout.add_widget(self.generate_button)

        # Кнопка "Назад"
        self.back_button = MDRaisedButton(
            text="Назад",
            on_press=self.back_button_pressed,
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            padding="5dp"
        )
        button_layout.add_widget(self.back_button)

        button_layout.add_widget(Widget(size_hint_x=0.1))

        # Кнопки переключения скриптов
        self.ivr_button = MDRaisedButton(
            text="IVR",
            on_press=lambda x: self.switch_script("ivr"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1},
            padding="5dp"
        )
        button_layout.add_widget(self.ivr_button)

        self.ivr_to_inc_button = MDRaisedButton(
            text="IVRTOINC",
            on_press=lambda x: self.switch_script("ivr_to_inc"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1},
            padding="5dp"
        )
        button_layout.add_widget(self.ivr_to_inc_button)


        self.ivr_lv_button = MDRaisedButton(
            text="IVRLV",
            on_press=lambda x: self.switch_script("ivr_lv"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1},
            padding="5dp"
        )
        button_layout.add_widget(self.ivr_lv_button)

        self.inc_button = MDRaisedButton(
            text="INC",
            on_press=lambda x: self.switch_script("inc"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1},
            padding="5dp"
        )
        button_layout.add_widget(self.inc_button)

        self.inc_to_ivr_button = MDRaisedButton(
            text="INCTOIVR",
            on_press=lambda x: self.switch_script("inc_to_ivr"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1},
            padding="5dp"
        )
        button_layout.add_widget(self.inc_to_ivr_button)

        self.del_button = MDRaisedButton(
            text="DEL",
            on_press=lambda x: self.switch_script("del"),
            font_name=Styles.ENTRY_FONT,
            theme_text_color="Custom",
            text_color=Styles.BUTTON_TEXT_COLOR,
            md_bg_color=Styles.BUTTON_COLOR,
            pos_hint={"right": 1},
            padding="5dp"
        )
        button_layout.add_widget(self.del_button)

    def generate_query(self, instance):
        input_text = self.numbers_field.text.strip()
        if not input_text:
            return
        self.scripts[self.current_script]["generate_function"]()

    def generate_ivr_query(self):
        input_text = self.numbers_field.text.strip()
        if not input_text:
            return
        context = self.context_field.text
        client = self.client_field.text
        ivr_file = self.ivr_field.text
        numbers = self.numbers_field.text.splitlines()

        res = "INSERT INTO extensions (context, exten, priority, app, appdata) VALUES"
        for number in numbers:
            res += f"('{context}', '{number.strip()}', '1', 'Log', 'NOTICE, incomming for {client}'),"
            res += f"('{context}', '{number.strip()}', '2', 'Answer', ''),"
            res += f"('{context}', '{number.strip()}', '3', 'Wait', '1'),"
            res += f"('{context}', '{number.strip()}', '4', 'Playback', '{ivr_file},skip'),"
            res += f"('{context}', '{number.strip()}', '5', 'Hangup', ''),"
        res = res[:-1] + ';'
        self.output_field.text = res

    def generate_ivr_to_inc_query(self):
        input_text = self.numbers_field.text.strip()
        if not input_text:
            return
        context = self.context_field.text
        prefix = self.prefix_field.text
        numbers = self.numbers_field.text.splitlines()

        res = ''
        for number in numbers:
            res += f"DELETE FROM extensions WHERE exten = '{number.strip()}' AND context = '{context}';"
            res += f"INSERT INTO extensions (context, exten, priority, app, appdata) VALUES"
            res += f"('{context}', '{number.strip()}', '1', 'Log', 'NOTICE, incomming'),"
            res += f"('{context}', '{number.strip()}', '2', 'Dial', 'SIP/mediacore/{prefix}${{{number.strip()}}}',60),"
            res += f"('{context}', '{number.strip()}', '3', 'Hangup', '');"
        self.output_field.text = res

    def generate_ivr_lv_query(self):
        input_text = self.numbers_field.text.strip()
        if not input_text:
            return
        context = self.context_field.text
        client = self.client_field.text
        ivr_file = self.ivr_field.text
        numbers = self.numbers_field.text.splitlines()

        res = "INSERT INTO extensions (context, exten, priority, app, appdata) VALUES"
        for number in numbers:
            res += f"('{context}', '{number.strip()}', '1', 'Log', 'NOTICE, incomming for {client}'),"
            res += f"('{context}', '{number.strip()}', '2', 'Answer', ''),"
            res += f"('{context}', '{number.strip()}', '3', 'Wait', '1'),"
            res += f"('{context}', '{number.strip()}', '4', 'Playback', '{ivr_file},skip'),"
            res += f"('{context}', '{number.strip()}', '5', 'Hangup', ''),"
        res = res[:-1] + ';'
        self.output_field.text = res

    def generate_inc_query(self):
        input_text = self.numbers_field.text.strip()
        if not input_text:
            return
        context = self.context_field.text
        client = self.client_field.text
        prefix = self.prefix_field.text
        numbers = self.numbers_field.text.splitlines()

        res = "INSERT INTO extensions (context, exten, priority, app, appdata) VALUES"
        for number in numbers:
            res += f"('{context}', '{number.strip()}', '1', 'Log', 'NOTICE, for {client}'),"
            res += f"('{context}', '{number.strip()}', '2', 'Dial', 'SIP/mediacore/{prefix}${{{number.strip()}}}',60),"
            res += f"('{context}', '{number.strip()}', '3', 'Hangup', ''),"
        res = res[:-1] + ';'
        self.output_field.text = res

    def generate_inc_to_ivr_query(self):
        input_text = self.numbers_field.text.strip()
        if not input_text:
            return
        context = self.context_field.text
        ivr_file = self.ivr_field.text
        numbers = self.numbers_field.text.splitlines()

        res = ''
        for number in numbers:
            res += f"DELETE FROM extensions WHERE exten = '{number.strip()}' AND context = '{context}';"
            res += f"INSERT INTO extensions (context, exten, priority, app, appdata) VALUES"
            res += f"('{context}', '{number.strip()}', '1', 'Log', 'NOTICE, incomming'),"
            res += f"('{context}', '{number.strip()}', '2', 'Answer', ''),"
            res += f"('{context}', '{number.strip()}', '3', 'Wait', '1'),"
            res += f"('{context}', '{number.strip()}', '4', 'Playback', '{ivr_file},skip'),"
            res += f"('{context}', '{number.strip()}', '5', 'Hangup', '');"
        self.output_field.text = res

    def generate_del_query(self):
        input_text = self.numbers_field.text.strip()
        if not input_text:
            return
        context = self.context_field.text
        numbers = self.numbers_field.text.splitlines()

        res = ''
        for number in numbers:
            res += f"DELETE FROM extensions WHERE exten = '{number.strip()}' AND context = '{context}';"
        self.output_field.text = res

    def switch_script(self, script_name):
        self.current_script = script_name
        script_info = self.scripts[script_name]
        self.title_label.text = script_info["title"]
        self.context_label.text = script_info["context_label"]
        self.context_field.hint_text = script_info["context_hint"]
        self.client_label.text = script_info["client_label"]
        self.client_field.hint_text = script_info["client_hint"]
        self.prefix_label.text = script_info["prefix_label"]
        self.prefix_field.hint_text = script_info["prefix_hint"]
        self.ivr_label.text = script_info["ivr_label"]
        self.ivr_field.hint_text = script_info["ivr_hint"]
        self.scripts[script_name]["generate_function"] = getattr(self, f"generate_{script_name}_query")
        # Добавьте условия для других скриптов

    def back_button_pressed(self, instance):
        self.manager.current = "main"