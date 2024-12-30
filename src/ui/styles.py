import customtkinter as ctk


class Styles:
    @staticmethod
    def get_button_style(theme, variant="primary"):
        if variant == "primary":
            return {
                "fg_color": theme["accent"],
                "hover_color": theme["accent"],
                "text_color": theme["fg_primary"],
                "height": 36,
                "corner_radius": 8,
            }
        return {
            "fg_color": "transparent",
            "hover_color": theme["bg_tertiary"],
            "text_color": theme["fg_primary"],
            "height": 36,
            "corner_radius": 8,
            "border_width": 1,
        }

    @staticmethod
    def get_frame_style(theme, variant="primary"):
        if variant == "primary":
            return {"fg_color": theme["bg_primary"], "corner_radius": 10}
        return {"fg_color": theme["bg_secondary"], "corner_radius": 10}

    @staticmethod
    def get_text_style(theme, variant="normal"):
        styles = {
            "normal": {"font": ctk.CTkFont(size=13)},
            "small": {"font": ctk.CTkFont(size=11)},
            "large": {"font": ctk.CTkFont(size=16)},
            "title": {"font": ctk.CTkFont(size=20, weight="bold")},
            "subtitle": {"font": ctk.CTkFont(size=15, weight="bold")},
        }
        return styles[variant]
