import customtkinter as ctk
import theme

class NotesTab:
    def __init__(self, main_app):
        self.main_app = main_app
        self.root = main_app.root
        self.create_ui()
        self.load_notes()

    def create_ui(self):
        self.stats_frame = ctk.CTkFrame(self.root, corner_radius=16, fg_color="transparent") # you must have fg_color = "transparent" to prevent the grey background

        control_bar = ctk.CTkFrame(self.stats_frame, fg_color=theme.BG_CONTAINER, height=60, corner_radius=12)
        control_bar.pack(fill="x", pady=(0, 20), padx=5)

        # Title
        title = ctk.CTkLabel(
            control_bar,
            text="📝 Notes",
            font=("Arial", 20, "bold")
        )
        title.pack(side="left", padx=20, pady=10)

        # Text area (THIS is the note interface)
        self.textbox = ctk.CTkTextbox(
            self.stats_frame,
            fg_color=theme.BG_CONTAINER,
            wrap="word"
        )
        self.textbox.pack(
            padx=5,
            pady=(0,10), # don't do top y padding for the main content frame
            fill="both",
            expand=True
        )

    def show(self):
        """Display the stats tab"""
        self.stats_frame.pack(pady=20, padx=16, fill="both", expand=True)

    def hide(self):
        self.stats_frame.pack_forget()

    def save_notes(self):
        text = self.textbox.get("1.0", "end-1c")
        with open("notes.txt", "w", encoding="utf-8") as f:
            f.write(text)

    def load_notes(self):
        try:
            with open("notes.txt", "r", encoding="utf-8") as f:
                self.textbox.insert("1.0", f.read())
        except FileNotFoundError:
            pass
