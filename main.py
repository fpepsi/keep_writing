import tkinter as tk
from tkinter import messagebox
import threading
import time

class WritingChallenge:
    def __init__(self, root):
        self.root = root
        self.root.title("The Writing Challenge")
        self.root.geometry("1200x800")

        # Main frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Text widget
        self.text_widget = tk.Text(self.frame, wrap=tk.WORD, bg="white", font=("Arial", 16))
        self.text_widget.insert("1.0", "Start typing your text here...")
        self.text_widget.focus_set()
        self.text_widget.mark_set("insert", "1.0")
        self.text_widget.bind("<Key>", self.on_key_press)
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Timers
        self.main_timer_duration = 60  # 1 minute
        self.secondary_timer_limit = 10  # 10 seconds
        self.secondary_timer = None
        self.main_timer = None
        self.start_time = None
        self.secondary_start_time = None
        self.text_placeholder_active = True

    def on_key_press(self, event):
        if self.text_placeholder_active:
            self.text_widget.delete("1.0", tk.END)
            self.text_placeholder_active = False

        self.reset_secondary_timer()
        # Delete all tags from the text widget
        for tag in self.text_widget.tag_names():
            self.text_widget.tag_delete(tag)

        if not self.start_time:
            self.start_main_timer()
            self.start_secondary_timer()

    def reset_secondary_timer(self):
        self.secondary_start_time = time.time()

    def start_main_timer(self):
        self.start_time = time.time()
        self.main_timer = threading.Thread(target=self.run_main_timer)
        self.main_timer.daemon = True
        self.main_timer.start()

    def run_main_timer(self):
        while time.time() - self.start_time < self.main_timer_duration:
            time.sleep(1)
        self.display_popup("Congratulations, you made it!")

    def start_secondary_timer(self):
        self.secondary_start_time = time.time()
        self.secondary_timer = threading.Thread(target=self.run_secondary_timer)
        self.secondary_timer.daemon = True
        self.secondary_timer.start()

    def run_secondary_timer(self):
        while True:
            elapsed = time.time() - self.secondary_start_time

            if elapsed >= 4:
                self.text_widget.tag_add("orange", "1.0", tk.END)
                self.text_widget.tag_configure("orange", foreground="orange")

            if elapsed >= 7:
                self.text_widget.tag_add("red", "1.0", tk.END)
                self.text_widget.tag_configure("red", foreground="red")

            if elapsed >= self.secondary_timer_limit:
                self.display_popup("Game Over, you have not typed anything for the past 10 seconds!")
                break

            time.sleep(1)

    def display_popup(self, message):
        def on_play_again():
            self.reset_game()
            popup.destroy()

        def on_quit():
            self.root.destroy()

        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        popup.geometry("300x150")

        label = tk.Label(popup, text=message, wraplength=280)
        label.pack(pady=10)

        play_again_btn = tk.Button(popup, text="Play Again", command=on_play_again)
        play_again_btn.pack(side=tk.LEFT, padx=20)

        quit_btn = tk.Button(popup, text="Quit", command=on_quit)
        quit_btn.pack(side=tk.RIGHT, padx=20)

    def reset_game(self):
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", "Start typing your text here...")
        self.text_widget.tag_delete("orange")
        self.text_widget.tag_delete("red")
        self.text_placeholder_active = True
        self.start_time = None
        self.secondary_start_time = None

if __name__ == "__main__":
    root = tk.Tk()
    app = WritingChallenge(root)
    root.mainloop()
