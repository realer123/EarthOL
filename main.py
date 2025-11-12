import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from task_manager import TaskManager
from player_profile import Player


class TaskManagerApp:
    def __init__(self):
        self.manager = TaskManager("tasks.json")
        self.player = Player("Unknown Player")
        self.root = tk.Tk()
        self.root.title("Earth Online")
        self.root.geometry("800x600")

        # Fade animation variables
        self.alpha = 0
        self.fade_in = True
        self.current_text_index = 0
        self.texts = ["People love video games, The thrill of leveling up",
                      "Unlocking new skills, Watching numbers rise",
                      "But in chasing virtual progress",
                      "How many of us forget the greatest game of all",
                      "Running for 4.57 billion years",
                      "Across 197 servers", "With over 8 billion active players",
                      "And a map spanning 510 million square kilometers",
                      "No respawns, No cheating, One account for lifetime",
                      "Welcome to Earth Online", "This application is your interface to life itself",
                      "A productivity tracker and task visualizer designed",
                      "to help you level up in the only game that truly matters",
                      "Let's get started"]

        # --- Notebook (tabs) ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Tabs
        self.tab_home = tk.Frame(self.notebook, bg='black')
        self.tab_tasks = tk.Frame(self.notebook, bg='black')
        self.tab_ftasks = tk.Frame(self.notebook, bg='black')
        self.tab_stats = tk.Frame(self.notebook, bg='black')
        self.tab_reminder = tk.Frame(self.notebook, bg='black')
        self.tab_note = tk.Frame(self.notebook, bg='black')
        self.tab_journal = tk.Frame(self.notebook, bg='black')
        self.tab_calender = tk.Frame(self.notebook, bg='black')

        self.notebook.add(self.tab_home, text="Home")
        self.notebook.add(self.tab_tasks, text="Today's Tasks")
        self.notebook.add(self.tab_ftasks, text="Upcoming Tasks")
        self.notebook.add(self.tab_stats, text="Stats")
        self.notebook.add(self.tab_reminder, text="Reminder")
        self.notebook.add(self.tab_note, text="Note Book")
        self.notebook.add(self.tab_journal, text="Journal")
        self.notebook.add(self.tab_calender, text="Calendar")

        # =============================
        # TAB 1: HOME
        # =============================
        # Create the label on the Home tab
        self.welcome_label = tk.Label(
            self.tab_home,
            text=self.texts[self.current_text_index],
            font=("Arial", 18),
            fg='white',
            bg='black'
        )
        self.welcome_label.pack(pady=40)

        # Start the fade animation
        self.update_fade()

        # =============================
        # TAB 2: TASK MANAGEMENT
        # =============================

        # Buttons
        button_frame = tk.Frame(self.tab_tasks, bg="black")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Add Task", command=self.open_add_task_window).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Mark Done", command=self.mark_done).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete All", command=self.delete_all_tasks).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Refresh", command=self.load_tasks).pack(side=tk.LEFT, padx=5)

        # Task Listbox with complete dark theme
        self.task_listbox = tk.Listbox(
            self.tab_tasks,
            width=75,
            height=15,
            bg='black',
            fg='white',
            selectforeground='white',
            highlightbackground='black',  # Match the background color
            borderwidth=0  # Remove any border
        )
        self.task_listbox.pack(pady=10)

        # Load tasks
        self.load_tasks()

        # =============================
        # TAB 3: STATS
        # =============================
        stats_frame = tk.Frame(self.tab_stats, bg='black')
        stats_frame.pack(pady=10)

        label_style = {'fg': 'white', 'bg': 'black'}

        tk.Label(stats_frame, text="Completed Tasks:", font=("Arial", 11, "bold"), **label_style).grid(row=0, column=0, sticky="w")
        tk.Label(stats_frame, text="n", **label_style).grid(row=0, column=1, sticky="w")

        #spacer
        tk.Label(stats_frame, text="").grid(row=1, column=0, pady=10)

        tk.Label(stats_frame, text="Intelligence", font=("Arial", 11, "bold"), **label_style).grid(row=2, column=0, sticky="w")
        tk.Label(stats_frame, text=self.player.intelligence, **label_style).grid(row=2, column=1, sticky="w")

        tk.Label(stats_frame, text="Knowledge", font=("Arial", 11, "bold"), **label_style).grid(row=3, column=0, sticky="w")
        tk.Label(stats_frame, text=self.player.knowledge, **label_style).grid(row=3, column=1, sticky="w")

        tk.Label(stats_frame, text="Social&Emotional", font=("Arial", 11, "bold"), **label_style).grid(row=4, column=0, sticky="w")
        tk.Label(stats_frame, text=self.player.SE, **label_style).grid(row=4, column=1, sticky="w")

        tk.Label(stats_frame, text="Atheleticism", font=("Arial", 11, "bold"), **label_style).grid(row=5, column=0, sticky="w")
        tk.Label(stats_frame, text=self.player.athleticism, **label_style).grid(row=5, column=1, sticky="w")

        tk.Label(stats_frame, text="Combat", font=("Arial", 11, "bold"), **label_style).grid(row=6, column=0, sticky="w")
        tk.Label(stats_frame, text=self.player.combat, **label_style).grid(row=6, column=1, sticky="w")

        tk.Label(stats_frame, text="Artistry", font=("Arial", 11, "bold"), **label_style).grid(row=7, column=0, sticky="w")
        tk.Label(stats_frame, text=self.player.artistry, **label_style).grid(row=7, column=1, sticky="w")

        tk.Label(stats_frame, text="Looks", font=("Arial", 11, "bold"), **label_style).grid(row=8, column=0, sticky="w")
        tk.Label(stats_frame, text=self.player.looks, **label_style).grid(row=8, column=1, sticky="w")

    # --------------------------
    # Fade Animation Method - FIXED COLOR FORMAT
    # --------------------------
    def update_fade(self):
        # check if last element, if true we just make it hold
        if self.current_text_index >= len(self.texts) - 1 and self.alpha >= 1:
            # Ensure the last text stays fully visible
            self.welcome_label.config(fg='#ffffff')
            return

        if self.fade_in:
            self.alpha += 0.05
            if self.alpha >= 1:
                self.alpha = 1
                self.fade_in = False
                # When fully faded in, wait a bit before fading out
                self.root.after(1000, self.update_fade)
                return
        else:
            self.alpha -= 0.05
            if self.alpha <= 0:
                self.alpha = 0
                self.fade_in = True
                # When fully faded out, switch to next text
                self.current_text_index += 1

                # Check if we've reached the end of the list
                if self.current_text_index >= len(self.texts):
                    # Stop the animation by not calling update_fade again
                    self.alpha = 1
                    return

                self.welcome_label.config(text=self.texts[self.current_text_index])

        # FIXED: Use grayscale color instead of alpha transparency
        # Convert alpha to grayscale value (0-255)
        gray_value = int(self.alpha * 255)
        color = f'#{gray_value:02x}{gray_value:02x}{gray_value:02x}'

        self.welcome_label.config(fg=color)
        self.root.after(50, self.update_fade)

    # --------------------------
    # Add Task Popup
    # --------------------------
    def open_add_task_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Task")
        add_window.geometry("350x320")

        # --- Labels and Inputs ---
        tk.Label(add_window, text="Task Name:").pack()
        name_entry = tk.Entry(add_window, width=30)
        name_entry.pack(pady=5)

        tk.Label(add_window, text="Category:").pack()
        category_options = [
            "School Work",
            "Self-Study-STEM",
            "Self-Study-Humanities",
            "Workout",
            "Combat Training",
            "Looks",
            "Practice Music",
            "Practice Arts",
            "Play Sports",
            "Others"
        ]
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(
            add_window, textvariable=category_var, values=category_options, state="readonly"
        )
        category_dropdown.pack(pady=5)
        category_dropdown.current(0)

        tk.Label(add_window, text="Scheduled Time:").pack()
        time_entry = tk.Entry(add_window, width=30)
        time_entry.pack(pady=5)

        #-------------------------duration------------------------------#

        tk.Label(add_window, text="Duration in minutes:").pack(pady=5)

        # Validation function — allows only empty string or digits
        def validate_integer_input(new_value):
            return new_value.isdigit() or new_value == ""

        # Register the validation command with Tkinter
        vcmd = add_window.register(validate_integer_input)

        # Entry with validation enabled
        duration_entry = tk.Entry(
            add_window,
            width=30,
            validate="key",
            validatecommand=(vcmd, "%P")  # %P = the new proposed value after keypress
        )
        duration_entry.pack(pady=5)
        #------------------------------------------------------------------------------

        tk.Label(add_window, text="Note:").pack()
        note_entry = tk.Entry(add_window, width=30)
        note_entry.pack(pady=5)

        # --- Save & Close ---
        def save_and_close():
            name = name_entry.get().strip()
            duration_str = duration_entry.get().strip()
            if not name:
                messagebox.showwarning("Warning", "Task name cannot be empty.")
                return
            if not duration_str:
                messagebox.showwarning("Warning", "Task duration must be set.")
                return

            try:
                duration = int(duration_str)
            except ValueError:
                messagebox.showerror("Invalid Input", "Duration must be a number.")
                return

            category = category_var.get()
            scheduled_time = time_entry.get().strip() or "No time"
            note = note_entry.get().strip() or ""

            self.manager.add_task(name, scheduled_time, category, duration, note)
            self.load_tasks()
            add_window.destroy()

        tk.Button(add_window, text="Add Task", command=save_and_close).pack(pady=10)


    # --------------------------
    # Task Actions
    # --------------------------
    def mark_done(self):
        try:
            # get selected task name
            selection = self.task_listbox.get(self.task_listbox.curselection())
            name = selection.split(" | ")[0].replace("✅", "").replace("⬜", "").strip()
            task = self.manager.get_task(name)
            if not task:
                messagebox.showerror("Error", "Task not found.")
                return

            self.manager.mark_done(name)

            category = task.category

            if category == "School Work":
                # Ask user for additional data
                grade = simpledialog.askfloat("Grade", "Enter your grade (0–100):", parent=self.root, minvalue=0, maxvalue=100)
                target = simpledialog.askfloat("Target", "Enter your target grade (0–100):", parent=self.root, minvalue=0, maxvalue=100)
                weight = simpledialog.askfloat("Weight", "Enter assignment weight (0–1):", parent=self.root, minvalue=0, maxvalue=1)
                disc = self.player.discipline if hasattr(self.player, "discipline") else 0

                base = int(task.duration)
                raw_xp = base * (grade / 100) * ((grade - target) / 5) * (1 + disc) * weight
                if raw_xp < 0: raw_xp = 0  # prevent negative XP

                self.player.add_experience(raw_xp)
                self.player.intelligence += raw_xp * 0.4
                self.player.knowledge += raw_xp * 0.6
                messagebox.showinfo("XP Gained", f"You earned {raw_xp:.1f} XP from {category}.")

            else:
                # General focus rating popup
                self.ask_focus_rating(task, category)

        except Exception as e:
            messagebox.showerror("Error", f"Error marking task done: {e}")

    def ask_focus_rating(self, task, category):
        popup = tk.Toplevel(self.root)
        popup.title("Rate Your Focus")
        popup.geometry("250x180")
        popup.grab_set()

        tk.Label(popup, text=f"How focused were you on '{task.name}'?", wraplength=200).pack(pady=10)
        selected = tk.IntVar(value=0)
        for i in range(1, 5):
            tk.Radiobutton(popup, text=f"{i} - {'⭐' * i}", variable=selected, value=i).pack(anchor="w")

        def submit_rating():
            focus_rating = selected.get()
            if focus_rating == 0:
                messagebox.showwarning("Missing", "Please select a focus level.")
                return

            popup.destroy()
            raw_xp = task.duration * (1 + 0.08 * focus_rating ** 2)
            self.player.add_experience(raw_xp)

            # Attribute distribution by category
            if category == "Self-Study-STEM":
                self.player.intelligence += raw_xp * 0.6
                self.player.knowledge += raw_xp * 0.2
                self.player.discipline += raw_xp * 0.1

            elif category == "Self-Study-Humanities":
                self.player.intelligence += raw_xp * 0.1
                self.player.knowledge += raw_xp * 0.5
                self.player.SE += raw_xp * 0.1
                self.player.discipline += raw_xp * 0.3

            elif category == "Workout":
                self.player.athleticism += raw_xp * 0.6
                self.player.combat += raw_xp * 0.1
                self.player.discipline += raw_xp * 0.3

            elif category == "Combat Training":
                self.player.athleticism += raw_xp * 0.5
                self.player.combat += raw_xp * 0.4
                self.player.discipline += raw_xp * 0.1

            elif category == "Looks":
                self.player.discipline += raw_xp * 0.3
                self.player.confidence += raw_xp * 0.4

            elif category == "Practice Music":
                self.player.creativity += raw_xp * 0.6
                self.player.discipline += raw_xp * 0.2

            elif category == "Practice Arts":
                self.player.creativity += raw_xp * 0.7
                self.player.discipline += raw_xp * 0.2

            elif category == "Play Sports":
                self.player.athleticism += raw_xp * 0.5
                self.player.teamwork += raw_xp * 0.3

            else:  # Others
                self.player.discipline += raw_xp * 0.3

            messagebox.showinfo("XP Gained", f"You earned {raw_xp:.1f} XP from {category}.")

    def delete_task(self):
        try:
            selection = self.task_listbox.get(self.task_listbox.curselection())
            name = selection.split(" | ")[0].replace("✅", "").replace("⬜", "").strip()
            self.manager.delete_task(name)
            self.load_tasks()
        except tk.TclError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def delete_all_tasks(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
            self.manager.tasks = []
            self.manager.save_tasks()
            self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.manager.tasks:
            self.task_listbox.insert(tk.END, str(task))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TaskManagerApp()
    app.run()