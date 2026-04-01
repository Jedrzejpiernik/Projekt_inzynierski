import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import pandas as pd

# --- Funkcje pomocnicze ---
def clear_folder(folder_path):
    """Czyści zawartość folderu przed zapisem nowych plików."""
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Błąd przy usuwaniu {file_path}. Szczegóły: {e}')

def trim_video():
    """Ładowanie filmu i podział na 30-sekundowe fragmenty."""
    video_path = filedialog.askopenfilename(title="Wybierz plik wideo")
    if not video_path:
        messagebox.showerror("Błąd", "Nie wybrano pliku wideo.")
        return

    output_folder = os.path.join(os.getcwd(), "trimmed_videos")
    os.makedirs(output_folder, exist_ok=True)
    subprocess.run(["python", "trimmer.py", video_path, output_folder])
    instructions.set("Podzielono film na fragmenty 30-sekundowe. Przejdź do podziału na klatki.")

def extract_frames():
    """Podział filmu na klatki."""
    input_folder = "C:/Users/jszcz/PycharmProjects/inzynierkav1/trimmed_videos"

    if not os.path.exists(input_folder) or not os.listdir(input_folder):
        messagebox.showerror("Błąd", "Folder 'trimmed_videos' jest pusty lub nie istnieje.")
        return

    video_file = filedialog.askopenfilename(
        initialdir=input_folder,
        title="Wybierz plik MP4 do podziału na klatki",
        filetypes=[("Pliki MP4", "*.mp4")]
    )

    if not video_file:
        messagebox.showerror("Błąd", "Nie wybrano pliku MP4.")
        return

    output_folder = r"C:\Users\jszcz\PycharmProjects\inzynierkav1\yolov5\data\images"
    clear_folder(output_folder)

    # Przekazuje pełną ścieżkę do pliku wideo
    subprocess.run(["python", "klatki.py", video_file, output_folder])
    instructions.set("Podzielono film na klatki. Możesz uruchomić detekcję.")

def run_detection():
    """Uruchamia YOLO na podzielonych klatkach."""
    instructions.set("Trwa detekcja YOLO... Czekaj.")
    # Ważne: to okno może na chwilę "zamrozić" GUI w trakcie działania, to normalne przy subprocess.run
    root.update()
    subprocess.run(["python", "uruchamianie.py"])
    instructions.set("Detekcja zakończona. Przejdź do trackera.")

def run_tracker():
    """Uruchamia tracker na wynikach detekcji."""
    instructions.set("Trwa śledzenie obiektów...")
    root.update()
    subprocess.run(["python", "tracker.py"])
    instructions.set("Śledzenie zakończone. Możesz sprawdzić adnotacje.")

def verify_annotations():
    """
    Krok 5: Uruchamia narzędzie do weryfikacji i usuwania błędów (tracking.py).
    """
    instructions.set("Uruchamianie narzędzia weryfikacji...")
    subprocess.run(["python", "tracking.py"])
    instructions.set("Weryfikacja zakończona. Jeśli dane są poprawne, przejdź do wizualizacji.")

def visualize_final_trajectories():
    """
    Krok 6: Uruchamia finalną wizualizację trajektorii (trajektorie.py).
    """
    instructions.set("Generowanie wykresu trajektorii...")
    subprocess.run(["python", "trajektorie.py"])
    instructions.set("Wykres wygenerowany.")

# --- GUI ---
root = tk.Tk()
root.title("GUI do analizy filmów i trajektorii")
# Zwiększyłem nieco wysokość okna, żeby zmieścił się dodatkowy przycisk
root.geometry("600x480")

instructions = tk.StringVar()
instructions.set("Załaduj film, aby rozpocząć proces.")

label_instructions = tk.Label(root, textvariable=instructions, wraplength=500, justify="center")
label_instructions.pack(pady=20)

# Lista przycisków
btn_trim = tk.Button(root, text="1. Podziel film na 30s fragmenty", command=trim_video, width=40)
btn_trim.pack(pady=5)

btn_extract = tk.Button(root, text="2. Podziel fragmenty na klatki", command=extract_frames, width=40)
btn_extract.pack(pady=5)

btn_detect = tk.Button(root, text="3. Uruchom detekcję YOLO", command=run_detection, width=40)
btn_detect.pack(pady=5)

btn_track = tk.Button(root, text="4. Uruchom tracker", command=run_tracker, width=40)
btn_track.pack(pady=5)

# ZMIANA: Przycisk 5 teraz służy do sprawdzania (uruchamia tracking.py)
btn_verify = tk.Button(root, text="5. Sprawdzenie adnotacji", command=verify_annotations, width=40)
btn_verify.pack(pady=5)

# NOWOŚĆ: Przycisk 6 do finalnej wizualizacji (uruchamia trajektorie.py)
btn_viz_final = tk.Button(root, text="6. Wizualizacja trajektorii", command=visualize_final_trajectories, width=40)
btn_viz_final.pack(pady=5)

btn_exit = tk.Button(root, text="Zakończ", command=root.quit, width=40, bg="#ffcccc") # Lekko czerwony dla wyróżnienia
btn_exit.pack(pady=20)

root.mainloop()