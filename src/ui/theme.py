# src/ui/theme.py
class AppTheme:
    # Color Schemes
    DARK = {
        "bg_primary": "#1a1a1a",
        "bg_secondary": "#2d2d2d",
        "bg_tertiary": "#404040",
        "fg_primary": "#ffffff",
        "fg_secondary": "#b3b3b3",
        "accent": "#007bff",
        "success": "#28a745",
        "warning": "#ffc107",
        "error": "#dc3545",
    }

    LIGHT = {
        "bg_primary": "#ffffff",
        "bg_secondary": "#f8f9fa",
        "bg_tertiary": "#e9ecef",
        "fg_primary": "#212529",
        "fg_secondary": "#6c757d",
        "accent": "#0056b3",
        "success": "#198754",
        "warning": "#ffc107",
        "error": "#dc3545",
    }

    @classmethod
    def setup_theme(cls, mode="dark"):
        import customtkinter as ctk

        theme = cls.DARK if mode == "dark" else cls.LIGHT

        # Configure CustomTkinter
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode(mode)

        return theme
