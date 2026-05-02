import customtkinter as ctk
import threading
import time
import tkinter as tk

class AnimationUtils:
    """Utility class for modern UI animations"""

    @staticmethod
    def fade_in(widget, duration=0.5, steps=20):
        """Fade in animation for widgets"""
        def animate():
            step_duration = duration / steps
            is_window = isinstance(widget, (tk.Tk, tk.Toplevel, ctk.CTkToplevel))
            for i in range(steps + 1):
                alpha = i / steps
                try:
                    if is_window:
                        widget.attributes("-alpha", alpha)
                    else:
                        widget.configure(fg_color=AnimationUtils._adjust_alpha(widget.cget("fg_color"), alpha))
                    widget.update()
                    time.sleep(step_duration)
                except:
                    break
        threading.Thread(target=animate, daemon=True).start()

    @staticmethod
    def fade_in_from_bottom(widget, duration=0.5, distance=30):
        """Fade in the widget from below"""
        def animate():
            steps = 20
            step_duration = duration / steps
            manager = widget.winfo_manager()
            original_padx = 0
            original_pady = 0
            if manager == "pack":
                info = widget.pack_info()
                original_padx = info.get("padx", 0)
                original_pady = info.get("pady", 0)
                if isinstance(original_padx, tuple):
                    original_padx = original_padx[0]
                if isinstance(original_pady, tuple):
                    original_pady = original_pady[0]
                original_padx = int(original_padx or 0)
                original_pady = int(original_pady or 0)
            elif manager == "grid":
                info = widget.grid_info()
                original_padx = info.get("padx", 0)
                original_pady = info.get("pady", 0)
                if isinstance(original_padx, tuple):
                    original_padx = original_padx[0]
                if isinstance(original_pady, tuple):
                    original_pady = original_pady[0]
                original_padx = int(original_padx or 0)
                original_pady = int(original_pady or 0)
            for i in range(steps + 1):
                progress = i / steps
                eased = 1 - (1 - progress) ** 2
                alpha = progress
                try:
                    if manager == "pack":
                        pady = original_pady - int(distance * eased)
                        widget.pack_configure(pady=pady)
                    elif manager == "grid":
                        pady = original_pady - int(distance * eased)
                        widget.grid_configure(pady=pady)
                    else:
                        current_x = widget.winfo_x()
                        current_y = widget.winfo_y()
                        widget.place(x=current_x, y=current_y - distance + int(distance * eased))
                    if hasattr(widget, 'configure'):
                        try:
                            widget.configure(fg_color=AnimationUtils._adjust_alpha(widget.cget("fg_color"), alpha))
                        except:
                            pass
                    widget.update()
                    time.sleep(step_duration)
                except:
                    break
        threading.Thread(target=animate, daemon=True).start()

    def fade_out(widget, duration=0.5, steps=20):
        """Fade out animation for widgets and windows"""
        def animate():
            step_duration = duration / steps
            is_window = isinstance(widget, (tk.Tk, tk.Toplevel, ctk.CTkToplevel))
            for i in range(steps, -1, -1):
                alpha = i / steps
                try:
                    if is_window:
                        widget.attributes("-alpha", alpha)
                    else:
                        widget.configure(fg_color=AnimationUtils._adjust_alpha(widget.cget("fg_color"), alpha))
                    widget.update()
                    time.sleep(step_duration)
                except:
                    break
        threading.Thread(target=animate, daemon=True).start()

    @staticmethod
    def slide_in(widget, direction="right", duration=0.3, distance=50):
        """Slide in animation for widgets"""
        def animate():
            steps = 20
            step_duration = duration / steps
            manager = widget.winfo_manager()
            original_padx = 0
            original_pady = 0
            if manager == "pack":
                info = widget.pack_info()
                original_padx = info.get("padx", 0)
                original_pady = info.get("pady", 0)
                if isinstance(original_padx, tuple):
                    original_padx = original_padx[0]
                if isinstance(original_pady, tuple):
                    original_pady = original_pady[0]
                original_padx = int(original_padx or 0)
                original_pady = int(original_pady or 0)
            elif manager == "grid":
                info = widget.grid_info()
                original_padx = info.get("padx", 0)
                original_pady = info.get("pady", 0)
                if isinstance(original_padx, tuple):
                    original_padx = original_padx[0]
                if isinstance(original_pady, tuple):
                    original_pady = original_pady[0]
                original_padx = int(original_padx or 0)
                original_pady = int(original_pady or 0)
            else:
                current_x = widget.winfo_x()
                current_y = widget.winfo_y()

            is_window = isinstance(widget, (tk.Tk, tk.Toplevel, ctk.CTkToplevel))
            window_width = widget.winfo_width() or widget.winfo_reqwidth()
            window_height = widget.winfo_height() or widget.winfo_reqheight()

            for i in range(steps + 1):
                progress = i / steps
                eased_progress = 1 - (1 - progress) ** 3

                try:
                    if manager == "pack":
                        padx = original_padx
                        pady = original_pady
                        if direction == "right":
                            padx = original_padx - distance + int(distance * eased_progress)
                        elif direction == "left":
                            padx = original_padx + distance - int(distance * eased_progress)
                        elif direction == "up":
                            pady = original_pady + distance - int(distance * eased_progress)
                        elif direction == "down":
                            pady = original_pady - distance + int(distance * eased_progress)
                        widget.pack_configure(padx=padx, pady=pady)
                    elif manager == "grid":
                        padx = original_padx
                        pady = original_pady
                        if direction == "right":
                            padx = original_padx - distance + int(distance * eased_progress)
                        elif direction == "left":
                            padx = original_padx + distance - int(distance * eased_progress)
                        elif direction == "up":
                            pady = original_pady + distance - int(distance * eased_progress)
                        elif direction == "down":
                            pady = original_pady - distance + int(distance * eased_progress)
                        widget.grid_configure(padx=padx, pady=pady)
                    else:
                        if direction == "right":
                            x = current_x - distance + (distance * eased_progress)
                            y = current_y
                        elif direction == "left":
                            x = current_x + distance - (distance * eased_progress)
                            y = current_y
                        elif direction == "up":
                            x = current_x
                            y = current_y + distance - (distance * eased_progress)
                        elif direction == "down":
                            x = current_x
                            y = current_y - distance + (distance * eased_progress)
                        if is_window:
                            widget.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
                        else:
                            widget.place(x=x, y=y)
                    widget.update()
                    time.sleep(step_duration)
                except:
                    break

        threading.Thread(target=animate, daemon=True).start()

    @staticmethod
    def pulse_button(widget, duration=0.2):
        """Pulse animation for buttons on click"""
        def animate():
            original_color = widget.cget("fg_color")
            lighter_color = AnimationUtils._lighten_color(original_color)

            # Pulse out
            widget.configure(fg_color=lighter_color)
            widget.update()
            time.sleep(duration/2)

            # Pulse back
            widget.configure(fg_color=original_color)
            widget.update()

        threading.Thread(target=animate, daemon=True).start()

    @staticmethod
    def bounce_in(widget, duration=0.6):
        """Bounce in animation for widgets"""
        def animate():
            steps = 30
            step_duration = duration / steps

            for i in range(steps + 1):
                progress = i / steps
                # Bounce easing function
                if progress < 0.5:
                    scale = 1 + (0.2 * (progress * 2))
                else:
                    scale = 1 + (0.2 * (1 - ((progress - 0.5) * 2)))

                try:
                    # Scale the widget (simplified - would need more complex implementation for full scaling)
                    widget.update()
                    time.sleep(step_duration)
                except:
                    break

        threading.Thread(target=animate, daemon=True).start()

    @staticmethod
    def typewriter_text(label, text, duration=2.0):
        """Typewriter effect for text"""
        def animate():
            label.configure(text="")
            delay = duration / len(text) if text else 0

            for i, char in enumerate(text):
                try:
                    label.configure(text=text[:i+1])
                    label.update()
                    time.sleep(delay)
                except:
                    break

        threading.Thread(target=animate, daemon=True).start()

    @staticmethod
    def _adjust_alpha(color_tuple, alpha):
        """Adjust alpha for color tuples (light, dark)"""
        if isinstance(color_tuple, tuple) and len(color_tuple) == 2:
            light, dark = color_tuple
            return (AnimationUtils._adjust_single_color_alpha(light, alpha),
                   AnimationUtils._adjust_single_color_alpha(dark, alpha))
        return color_tuple

    @staticmethod
    def _adjust_single_color_alpha(color, alpha):
        """Adjust alpha for single color"""
        # This is a simplified implementation
        # In a real implementation, you'd convert to RGBA and adjust alpha
        return color

    @staticmethod
    def _lighten_color(color_tuple):
        """Lighten a color tuple for pulse effect"""
        if isinstance(color_tuple, tuple) and len(color_tuple) == 2:
            light, dark = color_tuple
            return (AnimationUtils._lighten_single_color(light),
                   AnimationUtils._lighten_single_color(dark))
        return color_tuple

    @staticmethod
    def _lighten_single_color(color):
        """Lighten a single hex color"""
        # Simplified color lightening
        if color.startswith("#"):
            # Convert to lighter shade
            return "#4CAF50"  # Example lighter color
        return color

class AnimatedButton(ctk.CTkButton):
    """Enhanced button with click animation"""

    def __init__(self, *args, **kwargs):
        original_command = kwargs.pop("command", None)
        super().__init__(*args, **kwargs)
        self._original_command = original_command
        self.configure(command=self._animated_click)

    def _animated_click(self):
        AnimationUtils.pulse_button(self)
        if self._original_command:
            self.after(50, self._original_command)

    def set_command(self, command):
        """Set the command with animation"""
        self._original_command = command