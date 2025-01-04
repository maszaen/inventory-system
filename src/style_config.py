from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication


class Theme:
    @staticmethod
    def detect_system_theme():
        palette = QApplication.palette()
        window_color = palette.color(QPalette.Window)
        return window_color.lightness() < 128

    @staticmethod
    def get_theme_colors():
        is_dark = Theme.detect_system_theme()

        if is_dark:
            return {
                "background": "#1e1e1e",
                "border": "#3c3c3c",
                "card_bg": "#2d2d2d",
                "text_primary": "#ffffff",
                "text_secondary": "#888888",
                "accent": "#2563eb",
            }
        else:
            return {
                "background": "#f5f5f5",
                "border": "#e0e0e0",
                "card_bg": "#ffffff",
                "text_primary": "#000000",
                "text_secondary": "#666666",
                "accent": "#2563eb",
            }
