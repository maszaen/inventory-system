from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication
from PySide6.QtCharts import QChart


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
                "base": "#1e1e1e",
                "background": "#1e1e1e",
                "border": "#3c3c3c",
                "card_bg": "#2d2d2d",
                "text_primary": "#ffffff",
                "text_secondary": "#888888",
                "accent": "#2563eb",
                "bg_disabled": "#2d2d2d",
                "color_disabled": "#555555",
            }
        else:
            return {
                "base": "#f3f3f3",
                "background": "#f5f5f5",
                "border": "#e0e0e0",
                "card_bg": "#ffffff",
                "text_primary": "#000000",
                "text_secondary": "#666666",
                "accent": "#2563eb",
                "bg_disabled": "#e0e0e0",
                "color_disabled": "#a0a0a0",
            }

    @staticmethod
    def get_chart_theme():
        is_dark = Theme.detect_system_theme()
        if is_dark:
            return QChart.ChartThemeDark
        else:
            return QChart.ChartThemeLight

    @staticmethod
    def form():
        colors = Theme.get_theme_colors()
        return f"""
            QLineEdit {{
                background-color: {colors['background']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 5px;
                color: {colors['text_primary']};
            }}
        """

    @staticmethod
    def btn():
        colors = Theme.get_theme_colors()
        return f"""
            QPushButton {{
                background-color: #2563eb;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1d4ed8;
            }}
            QPushButton:disabled {{
                background-color: {colors['bg_disabled']};
                color: {colors['color_disabled']};
            }}
        """

    @staticmethod
    def btnmg():
        colors = Theme.get_theme_colors()
        return f"""
            QPushButton {{
                background-color: #2563eb;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                margin-top: 20px;
                color: white;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1d4ed8;
            }}
            QPushButton:disabled {{
                background-color: {colors['bg_disabled']};
                color: {colors['color_disabled']};
            }}
        """

    @staticmethod
    def border_btn():
        colors = Theme.get_theme_colors()
        return f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid {colors['text_secondary']};
                border-radius: 5px;
                padding: 8px 16px;
                color: {colors['text_secondary']};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {colors['background']};
                border: 2px solid {colors['text_primary']};
                color: {colors['text_primary']};
            }}
            QPushButton:disabled {{
                border-color: {colors['color_disabled']};
                color: {colors['color_disabled']};
            }}
        """

    @staticmethod
    def border_btn_sec():
        colors = Theme.get_theme_colors()
        return f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {colors['text_secondary']};
                border-radius: 5px;
                padding: 5px 16px;
                color: {colors['text_secondary']};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {colors['background']};
                border: 1px solid {colors['text_primary']};
                color: {colors['text_primary']};
            }}
            QPushButton:disabled {{
                border-color: {colors['color_disabled']};
                color: {colors['color_disabled']};
            }}
        """

    @staticmethod
    def green_btn():
        colors = Theme.get_theme_colors()
        return f"""
            QPushButton {{
                background-color: #22c55e;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #16a34a;
            }}
            QPushButton:disabled {{
                background-color: {colors['bg_disabled']};
                color: {colors['color_disabled']};
            }}
        """

    @staticmethod
    def green_btn2():
        colors = Theme.get_theme_colors()
        return f"""
            QPushButton {{
                background-color: #22c55e;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            QPushButton:hover {{
                background-color: #16a34a;
            }}
            QPushButton:disabled {{
                background-color: {colors['bg_disabled']};
                color: {colors['color_disabled']};
            }}
        """

    @staticmethod
    def txt_btn():
        return """
            QPushButton {
                border: none;
                color: #2563eb;
                text-decoration: underline;
                padding: 0px;
                font-size: 13px;
            }
            QPushButton:hover {
                color: #1d4ed8;
            }
        """

    @staticmethod
    def cbox():
        colors = Theme.get_theme_colors()
        return f"""
            QComboBox {{
                background-color: {colors['background']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 5px;
                color: {colors['text_primary']};
            }}
            QComboBox::drop-down {{
                border: none;
                background-color: {colors['background']};
            }}
        """

    @staticmethod
    def datepick():
        colors = Theme.get_theme_colors()
        return f"""
            QDateEdit {{
                background-color: {colors['background']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 5px;
                color: {colors['text_primary']};
            }}
            QDateEdit::drop-down {{
                border: none;
                background-color: {colors['border']};
            }}
        """
