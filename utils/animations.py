import customtkinter as ctk
import threading
import time

class AnimationUtils:
    """Utility class for modern UI animations"""

    @staticmethod
    def fade_in(widget, duration=0.5, steps=20):
        """Fade in animation for widgets"""
        def animate():
            step_duration = duration / steps
            for i in range(steps + 1):
                alpha = i / steps
                try:
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

            # Get current position
            current_x = widget.winfo_x()
            current_y = widget.winfo_y()

            for i in range(steps + 1):
                progress = i / steps
                # Ease out animation
                eased_progress = 1 - (1 - progress) ** 3

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

                try:
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
        super().__init__(*args, **kwargs)
        self.configure(command=self._animated_click)

    def _animated_click(self):
        AnimationUtils.pulse_button(self)
        # Call original command after animation
        if hasattr(self, '_original_command') and self._original_command:
            # Small delay to let animation start
            self.after(50, self._original_command)

    def set_command(self, command):
        """Set the command with animation"""
        self._original_command = command