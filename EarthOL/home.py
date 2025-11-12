class HomeTab:
    """
    Logic for the Home tab.
    Handles text progression and fade animation for welcome messages.
    """
    # how to use:
    # home_tab = HomeTab()
    # # In a UI loop or timer:
    # text, gray = home_tab.next_step()

    def __init__(self):
        # Texts to display on Home tab
        self.texts = [
            "People love video games, The thrill of leveling up",
            "Unlocking new skills, Watching numbers rise",
            "But in chasing virtual progress",
            "How many of us forget the greatest game of all",
            "Running for 4.57 billion years",
            "Across 197 servers",
            "With over 8 billion active players",
            "And a map spanning 510 million square kilometers",
            "No respawns, No cheating, One account for lifetime",
            "Welcome to Earth Online",
            "This application is your interface to life itself",
            "A productivity tracker and task visualizer designed",
            "to help you level up in the only game that truly matters",
            "Let's get started"
        ]

        # Fade animation state
        self.current_text_index = 0
        self.alpha = 0.0  # transparency simulation (0-1)
        self.fade_in = True

        # Current text (logic-only, UI should bind to this)
        self.current_text = self.texts[self.current_text_index]

    def next_step(self):
        """
        Simulate one step of the fade animation.
        Call repeatedly (e.g., via a timer in the UI).
        Returns the current text and a simulated grayscale color (0-255).
        """
        # Fade in/out logic
        if self.fade_in:
            self.alpha += 0.05
            if self.alpha >= 1:
                self.alpha = 1
                self.fade_in = False
        else:
            self.alpha -= 0.05
            if self.alpha <= 0:
                self.alpha = 0
                self.fade_in = True
                self.current_text_index += 1
                if self.current_text_index >= len(self.texts):
                    self.current_text_index = len(self.texts) - 1  # hold on last text

        # Update current text
        self.current_text = self.texts[self.current_text_index]

        # Convert alpha to grayscale value (0-255)
        gray_value = int(self.alpha * 255)
        return self.current_text, gray_value

    def jump_to_text(self, index):
        """Directly set which text to display."""
        if 0 <= index < len(self.texts):
            self.current_text_index = index
            self.current_text = self.texts[self.current_text_index]
            self.alpha = 1.0  # fully visible
            self.fade_in = False

    def reset_animation(self):
        """Reset the fade animation from the beginning."""
        self.current_text_index = 0
        self.alpha = 0.0
        self.fade_in = True
        self.current_text = self.texts[self.current_text_index]
