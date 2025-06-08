from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, QListWidgetItem, QSpacerItem, QSizePolicy, QApplication, QPlainTextEdit
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeySequence

class CountryCodeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_data()
        self.init_ui()

    def init_data(self):
        self.country_code_data = [
            ("Австралия	Australia", "61"),
            ("Австрия	Austria", "43"),
            ("Азербайджан	Azerbaijan", "994"),
            ("Албания	Albania", "355"),
            ("Алжир	Algeria", "213"),
            ("Ангола	Angola", "244"),
            ("Андорра	Andorra", "376"),
            ("Антигуа и Барбуда	Antigua and Barbuda", "1268"),
            ("Аргентина	Argentina", "54"),
            ("Армения	Armenia", "374"),
            ("Афганистан	Afghanistan", "93"),
            ("Багамские Острова	Bahamas", "1242"),
            ("Бангладеш	Bangladesh", "880"),
            ("Барбадос	Barbados", "1246"),
            ("Бахрейн	Bahrain", "973"),
            ("Белиз	Belize", "501"),
            ("Белоруссия	Belarus", "375"),
            ("Бельгия	Belgium", "32"),
            ("Бенин	Benin", "229"),
            ("Болгария	Bulgaria", "359"),
            ("Боливия	Bolivia", "591"),
            ("Босния и Герцеговина	Bosnia and Herzegovina", "387"),
            ("Ботсвана	Botswana", "267"),
            ("Бразилия	Brazil", "55"),
            ("Бруней	Brunei", "673"),
            ("Буркина-Фасо	Burkina Faso", "226"),
            ("Бурунди	Burundi", "257"),
            ("Бутан	Bhutan", "975"),
            ("Вануату	Vanuatu", "678"),
            ("Ватикан	Vatican", "3906698"),
            ("Великобритания	United Kingdom", "44"),
            ("Венгрия	Hungary", "36"),
            ("Венесуэла	Venezuela", "58"),
            ("Восточный Тимор	East Timor", "670"),
            ("Вьетнам	Vietnam", "84"),
            ("Габон	Gabon", "241"),
            ("Гаити	Haiti", "509"),
            ("Гайана	Guyana", "592"),
            ("Гамбия	Gambia", "220"),
            ("Гана	Ghana", "233"),
            ("Гватемала	Guatemala", "502"),
            ("Гвинея	Guinea", "224"),
            ("Гвинея-Бисау	Guinea Bissau", "245"),
            ("Германия	Germany", "49"),
            ("Гондурас	Honduras", "504"),
            ("Гренада	Grenada", "1473"),
            ("Греция	Greece", "30"),
            ("Грузия	Georgia", "995"),
            ("Дания	Denmark", "45"),
            ("Демократическая Республика Конго	Democratic Republic of the Congo", "243"),
            ("Джибути	Djibouti", "253"),
            ("Доминика	Dominica", "1767"),
            ("Доминиканская Республика	Dominican Republic", "1809,1829"),
            ("Египет	Egypt", "20"),
            ("Замбия	Zambia", "260"),
            ("Западная Сахара	Western Sahara", "213,212"),
            ("Зимбабве	Zimbabwe", "263"),
            ("Израиль	Israel", "972"),
            ("Индия	India", "91"),
            ("Индонезия	Indonesia", "62"),
            ("Иордания	Jordan", "962"),
            ("Ирак	Iraq", "964"),
            ("Иран	Iran", "98"),
            ("Ирландия	Ireland", "353"),
            ("Исландия	Iceland", "354"),
            ("Испания	Spain", "34"),
            ("Италия	Italy", "39"),
            ("Йемен	Yemen", "967"),
            ("Кабо-Верде	Cabo Verde", "238"),
            ("Казахстан	Kazakhstan", "77"),
            ("Камбоджа	Cambodia", "855"),
            ("Камерун	Cameroon", "237"),
            ("Канада	Canada", "1"),
            ("Катар	Qatar", "974"),
            ("Кения	Kenya", "254"),
            ("Кипр	Cyprus", "357"),
            ("Киргизия	Kyrgyzstan", "996"),
            ("Кирибати	Kiribati", "686"),
            ("Китай	China", "86"),
            ("Колумбия	Colombia", "57"),
            ("Коморы	Comoros", "269"),
            ("Косово	Kosovo", "381"),
            ("Коста-Рика	Costa Rica", "506"),
            ("Кот-д'Ивуар	Cote dIvoire", "225"),
            ("Куба	Cuba", "53"),
            ("Кувейт	Kuwait", "965"),
            ("Лаос	Laos", "856"),
            ("Латвия	Latvia", "371"),
            ("Лесото	Lesotho", "266"),
            ("Либерия	Liberia", "231"),
            ("Ливан	Lebanon", "961"),
            ("Ливия	Libya", "218"),
            ("Литва	Lithuania", "370"),
            ("Лихтенштейн	Liechtenstein", "423"),
            ("Люксембург	Luxembourg", "352"),
            ("Маврикий	Mauritius", "230"),
            ("Мавритания	Mauritania", "222"),
            ("Мадагаскар	Madagascar", "261"),
            ("Македония	Macedonia", "389"),
            ("Малави	Malawi", "265"),
            ("Малайзия	Malaysia", "65"),
            ("Мали	Mali", "223"),
            ("Мальдивы	Maldives", "960"),
            ("Мальта	Malta", "356"),
            ("Марокко	Morocco", "212"),
            ("Маршалловы Острова	Marshall Islands", "692"),
            ("Мексика	Mexico", "52"),
            ("Микронезия	Micronesia", "691"),
            ("Мозамбик	Mozambique", "258"),
            ("Молдова	Moldova", "373"),
            ("Монако	Monaco", "377"),
            ("Монголия	Mongolia", "976"),
            ("Мьянма	Myanmar", "95"),
            ("Намибия	Namibia", "264"),
            ("Науру	Nauru", "674"),
            ("Непал	Nepal", "977"),
            ("Нигер	Niger", "227"),
            ("Нигерия	Nigeria", "234"),
            ("Нидерланды	Netherlands", "31"),
            ("Никарагуа	Nicaragua", "505"),
            ("Новая Зеландия	New Zealand", "64"),
            ("Норвегия	Norway", "47"),
            ("Объединенные Арабские Эмираты	United Arab Emirates", "971"),
            ("Оман	Oman", "968"),
            ("Пакистан	Pakistan", "92"),
            ("Палау	Palau", "680"),
            ("Панама	Panama", "507"),
            ("Папуа-Новая Гвинея	Papua New Guinea", "675"),
            ("Парагвай	Paraguay", "595"),
            ("Перу	Peru", "51"),
            ("Польша	Poland", "48"),
            ("Португалия	Portugal", "351"),
            ("Республика Конго	Republic of the Congo", "242"),
            ("Россия	Russia", "7"),
            ("Руанда	Rwanda", "250"),
            ("Румыния	Romania", "40"),
            ("Самоа	Samoa", "685"),
            ("Сан-Марино	San Marino", "3780549"),
            ("Сан-Томеи Принсипи	Sao Tome and Principe", "239"),
            ("Саудовская Аравия	Saudi Arabia", "966"),
            ("Свазиленд	Eswatini", "268"),
            ("Северная Корея	North Korea", "850"),
            ("Сейшельские Острова	Seychelles", "248"),
            ("Сенегал	Senegal", "221"),
            ("Сент-Винсент и Гренадины	Saint Vincent and the Grenadines", "1784"),
            ("Сент-Китс и Невис	Saint Kitts and Nevis", "1869"),
            ("Сент-Люсия	Saint Lucia", "1758"),
            ("Сербия	Serbia", "381"),
            ("Сингапур	Singapore", "65"),
            ("Сирия	Syria", "963"),
            ("Словакия	Slovakia", "421"),
            ("Словения	Slovenia", "386"),
            ("Соединенные Штаты Америки	United States of America", "1"),
            ("Соломоновы Острова	Solomon Islands", "677"),
            ("Сомали	Somalia", "252"),
            ("Судан	Sudan", "249"),
            ("Суринам	Suriname", "597"),
            ("Сьерра-Леоне	Sierra Leone", "232"),
            ("Таджикистан	Tajikistan", "992"),
            ("Таиланд	Thailand", "66"),
            ("Тайвань	Taiwan", "886"),
            ("Танзания	Tanzania", "255"),
            ("Того	Togo", "228"),
            ("Тонга	Tonga", "676"),
            ("Тринидади Тобаго	Trinidad and Tobago", "1868"),
            ("Тувалу	Tuvalu", "688"),
            ("Тунис	Tunisia", "216"),
            ("Туркменистан	Turkmenistan", "993"),
            ("Турция	Turkey", "90"),
            ("Уганда	Uganda", "256"),
            ("Узбекистан	Uzbekistan", "998"),
            ("Украина	Ukraine", "380"),
            ("Уругвай	Uruguay", "598"),
            ("Фиджи	Fiji", "679"),
            ("Филиппины	Philippines", "63"),
            ("Финляндия	Finland", "358"),
            ("Франция	France", "33"),
            ("Хорватия	Croatia", "385"),
            ("Центрально-африканская Республика	Central African Republic", "236"),
            ("Чад	Chad", "235"),
            ("Черногория	Montenegro", "382"),
            ("Чехия	Czech Republic", "420"),
            ("Чили	Chile", "56"),
            ("Швейцария	Switzerland", "41"),
            ("Швеция	Sweden", "46"),
            ("Шри-Ланка	Sri Lanka", "94"),
            ("Эквадор	Ecuador", "593"),
            ("Экваториальная Гвинея	Equatorial Guinea", "240"),
            ("Эль-Сальвадор	El Salvador", "503"),
            ("Эритрея	Eritrea", "291"),
            ("Эстония	Estonia", "372"),
            ("Эфиопия	Ethiopia", "251"),
            ("Южная Африка	South Africa", "27"),
            ("Южная Корея	South Korea", "82"),
            ("Южный Судан	South Sudan", "211"),
            ("Ямайка	Jamaica", "1876"),
            ("Япония	Japan", "81")
        ]
        
        # Для быстрого поиска
        self.code_to_country = {}
        self.country_to_codes = {}
        for country, codes_str in self.country_code_data:
            codes = [c.strip() for c in codes_str.split(',')]
            self.country_to_codes[country.lower()] = codes
            for code in codes:
                self.code_to_country[code] = country

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по стране или коду...")
        self.search_input.textChanged.connect(self.update_list)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        self.list_widget = QListWidget()
        main_layout.addWidget(self.list_widget, 2)
        self.update_list()

        main_layout.addWidget(QLabel("Введите номера (по одному в строке):"))
        self.numbers_input = QTextEdit()
        main_layout.addWidget(self.numbers_input, 1)

        main_layout.addWidget(QLabel("Результат:"))
        self.result_output = QPlainTextEdit()
        self.result_output.setReadOnly(True)
        main_layout.addWidget(self.result_output, 2)

        self.result_output.installEventFilter(self)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        main_layout.addLayout(button_layout)

        self.process_button = QPushButton("Обработать")
        self.process_button.clicked.connect(self.process_numbers)
        button_layout.addWidget(self.process_button)

        self.copy_codes_button = QPushButton("Копировать коды")
        self.copy_codes_button.clicked.connect(self.copy_codes_to_clipboard)
        button_layout.addWidget(self.copy_codes_button)

        self.back_button = QPushButton("Назад")
        button_layout.addWidget(self.back_button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer)

    def copy_codes_to_clipboard(self):
        text_to_copy = '\n'.join(self.list_widget.item(i).text() for i in range(self.list_widget.count()))
        clipboard = QApplication.clipboard()
        clipboard.setText(text_to_copy)

    def eventFilter(self, obj, event): # Перехватываем Ctrl+C для нормальной обработки
        if obj == self.result_output and event.type() == QEvent.KeyPress:
            if event.matches(QKeySequence.Copy):
                self.copy_plain_text()
                return True
        return super().eventFilter(obj, event)

    def copy_plain_text(self):
        text = self.result_output.toPlainText()
        QApplication.clipboard().setText(text)

    def update_list(self):
        text = self.search_input.text().strip().lower()
        self.list_widget.clear()
        for country, codes_str in self.country_code_data:
            codes = [c.strip() for c in codes_str.split(',')]
            if (text in country.lower()) or any(text in code for code in codes):
                item = QListWidgetItem(f"{country}\t{', '.join(codes)}")
                self.list_widget.addItem(item)

    def process_numbers(self):
        numbers = [line.strip() for line in self.numbers_input.toPlainText().splitlines() if line.strip()]
        results = []
        for num in numbers:
            found_country = self.find_country_by_number(num)
            results.append(f"{num}\t{found_country}")
        self.result_output.setPlainText('\n'.join(results))

    def find_country_by_number(self, number):
        number = number.lstrip('+')
        max_code_len = max(len(code) for code in self.code_to_country)
        for code_len in range(max_code_len, 0, -1):
            prefix = number[:code_len]
            if prefix in self.code_to_country:
                return self.code_to_country[prefix]
        return "Неизвестно"