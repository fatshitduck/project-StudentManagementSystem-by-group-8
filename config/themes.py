# Color Themes Configuration
# Format: (light_mode, dark_mode)

THEMES = {
    # Main colors
    "bg_primary": ("#f5f7fa", "#1b2d42"),      # Background
    "bg_secondary": ("#eef2f5", "#16213e"),    # Secondary background
    "bg_sidebar": ("#ffffff", "#0f3460"),       # Sidebar background
    "bg_topbar": ("#e8ecf1", "#1a3a52"),        # Top bar background
    
    # Text colors
    "text_primary": ("#2c3e50", "#e0e0e0"),    # Primary text
    "text_secondary": ("#7f8c8d", "#b0b0b0"),  # Secondary text
    
    # Accent colors
    "accent_primary": ("#3498db", "#00d4ff"),  # Primary accent (buttons)
    "accent_secondary": ("#2ecc71", "#1abc9c"), # Secondary accent
    "accent_danger": ("#e74c3c", "#ff6b6b"),   # Danger (delete)
    
    # UI Elements
    "button_primary": ("#3498db", "#00d4ff"),
    "button_secondary": ("#95a5a6", "#546e7a"),
    "button_hover": ("#2980b9", "#0099cc"),
    
    # Entry/Input
    "input_bg": ("#ffffff", "#263238"),
    "input_border": ("#bdc3c7", "#37474f"),
    
    # Table/Treeview
    "table_bg": ("#ffffff", "#1e293b"),
    "table_text": ("#2c3e50", "#e0e0e0"),
}

# Color Themes Configuration
# Format: (light_mode, dark_mode)

import customtkinter as ctk

THEMES = {
    # Main colors
    "bg_primary": ("#f5f7fa", "#1b2d42"),      # Background
    "bg_secondary": ("#eef2f5", "#16213e"),    # Secondary background
    "bg_sidebar": ("#ffffff", "#0f3460"),       # Sidebar background
    "bg_topbar": ("#e8ecf1", "#1a3a52"),        # Top bar background

    # Text colors
    "text_primary": ("#2c3e50", "#e0e0e0"),    # Primary text
    "text_secondary": ("#7f8c8d", "#b0b0b0"),  # Secondary text

    # Accent colors
    "accent_primary": ("#3498db", "#00d4ff"),  # Primary accent (buttons)
    "accent_secondary": ("#2ecc71", "#1abc9c"), # Secondary accent
    "accent_danger": ("#e74c3c", "#ff6b6b"),   # Danger (delete)

    # UI Elements
    "button_primary": ("#3498db", "#00d4ff"),
    "button_secondary": ("#95a5a6", "#546e7a"),
    "button_hover": ("#2980b9", "#0099cc"),

    # Entry/Input
    "input_bg": ("#ffffff", "#263238"),
    "input_border": ("#bdc3c7", "#37474f"),

}

def get_color(key, mode="dark"):
    """
    Get color based on theme key and mode.
    mode: "light" or "dark"
    Returns: (light_color, dark_color) tuple for customtkinter
    """
    if key in THEMES:
        light, dark = THEMES[key]
        return (light, dark)
    return ("#ffffff", "#1a1a1a")  # Default fallback

def toggle_theme():
    """Toggle between light and dark theme"""
    current = ctk.get_appearance_mode()
    if current == "Dark":
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Dark")

def get_current_theme():
    """Get current theme mode"""
    return ctk.get_appearance_mode().lower()

def apply_theme_to_widget(widget, color_key):
    """Apply theme color to a widget"""
    color = get_color(color_key)
    if hasattr(widget, 'configure'):
        widget.configure(fg_color=color)

