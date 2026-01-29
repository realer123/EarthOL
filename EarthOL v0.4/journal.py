import customtkinter as ctk
import tkinter as tk
from datetime import date, datetime
from tkinter import messagebox
from entry import JournalEntry
import json
import os
import theme

# ------------Global journal state variable----------------------
STATE_FILE = "journal_state.json"

def load_journal_state():
    today = date.today().isoformat()
    default_state = {"journaled": False, "last_date": today}
    if not os.path.exists(STATE_FILE):
        return default_state

    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)

        # RESET LOGIC: If the saved date isn't today, reset to False
        if state.get("last_date") != today:
            state = default_state
            save_journal_state(state)
        return state
    except:
        return default_state


def save_journal_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

# --- GLOBAL INITIALIZATION ---
_state = load_journal_state()
Journal = _state["journaled"]
_last_reset = date.today()

def mark_as_journaled():
    """Call this when a user successfully saves a journal entry"""
    global Journal
    Journal = True
    save_journal_state({"journaled": True, "last_date": date.today().isoformat()})

class JournalTab:
    def __init__(self, main_app):
        self.main_app = main_app
        self.root = main_app.root

        # Create frame and UI, but do NOT pack it
        self.stats_frame = ctk.CTkFrame(self.root, corner_radius=16)
        self.create_ui()

    def create_ui(self):
        """Create all UI elements for journal tab"""
        self.stats_frame = ctk.CTkFrame(self.root, corner_radius=16, fg_color="transparent")

        control_bar = ctk.CTkFrame(self.stats_frame, fg_color=theme.BG_CONTAINER, height=60, corner_radius=12)
        control_bar.pack(fill="x", pady=(0, 14), padx=5) # something is wrong with the padding here idk, 20-6 to compensate

        title_label = ctk.CTkLabel(
            control_bar,
            text="📓️ Journal",
            font = ctk.CTkFont(size=20, weight="bold"),
            text_color = theme.TEXT_PRIMARY
        ).pack(side="left", padx=20, pady=10)

        #Search Mechanism
        self.search_entry = ctk.CTkEntry(
            control_bar,
            placeholder_text="🔍 Filter by Date (YYYY-MM-DD)",
            width=200,
            fg_color=theme.BTN_BG,
            border_color=theme.BORDER_NORMAL,
            font=ctk.CTkFont(size=13)
        )
        self.search_entry.pack(side="right", padx=(5, 10), pady=10)

        # Bind the "KeyRelease" event to trigger the filter function
        self.search_entry.bind("<KeyRelease>", self.update_filter)

        # Force focus out when clicking outside (optional, but good UX, dw about it now)
        self.stats_frame.bind("<Button-1>", lambda event: self.root.focus())
        control_bar.bind("<Button-1>", lambda event: self.root.focus())

        ctk.CTkButton(
            control_bar,
            text="➕ New Entry",
            command=self.open_add_entry_window,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=theme.ACCENT_BLUE,
            hover_color="#0ea5e9",  # Slightly light blue
            height=32,
            corner_radius=8
        ).pack(side="right", padx=10)
        # 3. Scrollable Area for Entries
        self.entries_frame = ctk.CTkScrollableFrame(
            self.stats_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.entries_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Initial Load
        self.refresh_listbox()



    # -----------------------------
    # Add Entry Window
    # -----------------------------
    def open_add_entry_window(self):
        add_window = ctk.CTkToplevel(self.root)
        add_window.title("New Entry")
        add_window.geometry("300x200")
        add_window.grab_set()

        wrap = ctk.CTkFrame(add_window, corner_radius=12)
        wrap.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(wrap, text="Choose a Date:").pack(anchor="w", pady=(6, 2))
        date_entry = ctk.CTkEntry(wrap, width=300, placeholder_text="YYYY-MM-DD")
        date_entry.pack(pady=4)

        def open_entry_textbox():
            input_str = date_entry.get().strip()
            try:
                input_date = datetime.strptime(input_str, "%Y-%m-%d").date().isoformat()
            except ValueError:
                messagebox.showwarning("Warning", "Date format incorrect. Use YYYY-MM-DD.")
                return

            # 1. Close the date-picker window FIRST
            add_window.destroy()

            # 2. Open the entry window AFTER a tiny delay (100ms)
            # This ensures the old window is completely gone from the focus stack
            entry = JournalEntry(input_date, "")
            self.root.after(100, lambda: entry.open_textbox(self.root, refresh_callback=self.refresh_listbox))
            mark_as_journaled()

        ctk.CTkButton(wrap, text="Done", command=open_entry_textbox).pack(pady=12)

    # -----------------------------
    # Helpers
    # -----------------------------
    def show(self):
        self._check_reset() #check for journal refresh
        self.stats_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.refresh_listbox()

    def hide(self):
        self.stats_frame.pack_forget()

    def refresh_listbox(self, filter_date=None):
        #Clear existing cards
        for widget in self.entries_frame.winfo_children():
            widget.destroy()
        # Load all entries
        entries = JournalEntry.load()

        #Filter entries
        if filter_date:
            # Keep only entries where the date STARTS with the search text
            entries = [e for e in entries if e.input_date.startswith(filter_date)]

        if not entries:
            # Handle "No entries at all" or "No match found"
            msg = "No matching entries found." if filter_date else "No journal entries yet."
            ctk.CTkLabel(
                self.entries_frame,
                text=msg,
                text_color=theme.TEXT_MUTED,
                font=ctk.CTkFont(size=16)
            ).pack(pady=40)
            return

        # Create a card for each entry
        for entry in entries:
            self.create_entry_card(entry)

    def create_entry_card(self, entry):
        """Helper to draw a single entry card (Styled like Task Row)"""
        # Card Container
        card = ctk.CTkFrame(
            self.entries_frame,
            fg_color=theme.BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=theme.BORDER_NORMAL
        )
        card.pack(fill="x", pady=6, padx=5)
        # Info Frame (Left side)
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        def _open(e=None):
            self.open_entry(entry)

        date_label = ctk.CTkLabel(
            info_frame,
            text=entry.input_date,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=theme.TEXT_PRIMARY,
            anchor="w"
        )
        date_label.pack(fill="x")
        date_label.bind("<Button-1>", _open)  # Make text clickable

        # Preview Text, dw for now
        preview_text = entry.text[:60] + "..." if entry.text and len(entry.text) > 60 else entry.text
        preview_label = ctk.CTkLabel(
            info_frame,
            text=preview_text if preview_text else "(No content)",
            font=ctk.CTkFont(size=12),
            text_color=theme.TEXT_MUTED,
            anchor="w"
        )
        preview_label.pack(fill="x")
        preview_label.bind("<Button-1>", _open)  # Make text clickable
        # Delete Button (Right side, transparent with red hover)
        ctk.CTkButton(
            card,
            text="🗑",
            width=32,
            height=32,
            fg_color="transparent",
            hover_color=theme.ACCENT_RED,
            text_color=theme.TEXT_SECONDARY,
            font=ctk.CTkFont(size=16),
            command=lambda e=entry: self.delete_entry(e)
        ).pack(side="right", padx=15)



    def _check_reset(self):
        """Check if date changed while app was running"""
        global Journal, _last_reset
        today = date.today()
        if today != _last_reset:
            Journal = False
            _last_reset = today
            save_journal_state({"journaled": False, "last_date": today.isoformat()})

    # Placeholder methods for completeness
    def open_entry(self, entry=None):
            entry.open_textbox(self.root, refresh_callback=self.refresh_listbox)


    def delete_entry(self, entry=None):
        if not entry:
            return

        confirm = messagebox.askyesno("Confirm", f"Delete the entry for {entry.input_date}?")
        if not confirm:
            return
        # Load, Filter, Save
        all_entries = JournalEntry.load()
        # Filter out the one we want to delete
        updated_entries = [e for e in all_entries if e.input_date != entry.input_date]
        # Save back
        data = [e.to_dict() for e in updated_entries]
        with open("journal.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        self.refresh_listbox()

    def update_filter(self, *args):
        search_text = self.search_entry.get().strip()
        self.refresh_listbox(filter_date=search_text)

    def save_jounral(self):
        return






