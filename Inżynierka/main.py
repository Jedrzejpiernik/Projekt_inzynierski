import tkinter as tk
from tkinter import filedialog, messagebox


class SpermAnnotationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacja do Adnotacji Plemników")
        self.root.geometry("800x600")

        # Menu główne
        menu_frame = tk.Frame(root)
        menu_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        tk.Button(menu_frame, text="Załaduj wideo", command=self.load_video).pack(side=tk.LEFT, padx=5)
        tk.Button(menu_frame, text="Adnotuj klatkę", command=self.annotate_frame).pack(side=tk.LEFT, padx=5)
        tk.Button(menu_frame, text="Automatyczna detekcja", command=self.auto_detect).pack(side=tk.LEFT, padx=5)
        tk.Button(menu_frame, text="Zapisz adnotacje", command=self.save_annotations).pack(side=tk.LEFT, padx=5)
        tk.Button(menu_frame, text="Eksportuj dane", command=self.export_data).pack(side=tk.LEFT, padx=5)

        # Obszar wideo
        self.video_label = tk.Label(root, text="Obszar wideo", bg="black", width=80, height=20)
        self.video_label.pack(pady=10)

        # Pasek kontrolny wideo
        controls_frame = tk.Frame(root)
        controls_frame.pack(fill=tk.X, pady=5)

        tk.Button(controls_frame, text="Poprzednia klatka", command=self.prev_frame).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="Odtwórz/Pauza", command=self.play_pause).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="Następna klatka", command=self.next_frame).pack(side=tk.LEFT, padx=5)

        self.video_slider = tk.Scale(controls_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=400)
        self.video_slider.pack(side=tk.LEFT, padx=5)

        # Panel wyników
        results_frame = tk.Frame(root, bg="lightgrey")
        results_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        tk.Label(results_frame, text="Wyniki detekcji", bg="lightgrey").pack(anchor=tk.N)
        self.results_text = tk.Text(results_frame, width=30, height=20)
        self.results_text.pack(padx=5, pady=5)

        # Okno logów
        logs_frame = tk.Frame(root, bg="white")
        logs_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        self.logs_text = tk.Text(logs_frame, height=5, bg="white")
        self.logs_text.pack(fill=tk.X, padx=5, pady=5)
        self.log("Aplikacja gotowa do użycia.")

    def load_video(self):
        filepath = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
        if filepath:
            self.log(f"Załadowano wideo: {filepath}")
            # Tutaj można zaimplementować logikę ładowania wideo

    def annotate_frame(self):
        self.log("Adnotacja klatki...")
        # Tutaj można zaimplementować logikę adnotacji klatki

    def auto_detect(self):
        self.log("Automatyczna detekcja plemników...")
        # Tutaj można zaimplementować logikę automatycznej detekcji (np. YOLO)

    def save_annotations(self):
        self.log("Adnotacje zapisane.")
        # Tutaj można zaimplementować logikę zapisywania adnotacji

    def export_data(self):
        self.log("Dane wyeksportowane.")
        # Tutaj można zaimplementować logikę eksportowania danych

    def prev_frame(self):
        self.log("Poprzednia klatka.")

    def play_pause(self):
        self.log("Odtwórz/Pauza wideo.")

    def next_frame(self):
        self.log("Następna klatka.")

    def log(self, message):
        self.logs_text.insert(tk.END, message + "\n")
        self.logs_text.see(tk.END)


# Inicjalizacja aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = SpermAnnotationApp(root)
    root.mainloop()
