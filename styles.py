
class Styles:
    BACKGROUND_COLOR = "#222222"
    BUTTON_COLOR = "#FF6666"
    BUTTON_TEXT_COLOR = "#222222"
    ENTRY_FONT = "Roboto"
    TEXT_FONT = "Roboto"

def apply_styles(app):
    app.theme_cls.primary_palette = "Gray"
    app.theme_cls.accent_palette = "Gray"
    app.theme_cls.bg_color = Styles.BACKGROUND_COLOR