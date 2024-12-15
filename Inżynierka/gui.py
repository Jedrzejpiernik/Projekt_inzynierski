import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess


# Funkcje pomocnicze
def clear_folder(folder_path):
    """Czyści zawartość folderu przed zapisem nowych plików."""
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
    input_folder = "C:/Users/jszcz/PycharmProjects/inzynierkav1/frames_output"

    if not os.path.exists(input_folder) or not os.listdir(input_folder):
        messagebox.showerror("Błąd", "Folder 'frames_output' jest pusty lub nie istnieje.")
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
    subprocess.run(["python", "uruchamianie.py"])
    instructions.set("Detekcja zakończona. Przejdź do trackera.")


def run_tracker():
    """Uruchamia tracker na wynikach detekcji."""
    instructions.set("Trwa śledzenie obiektów...")
    subprocess.run(["python", "tracker.py"])
    instructions.set("Śledzenie zakończone. Możesz wizualizować trajektorie.")


def visualize_trajectories():
    """Wizualizuje trajektorie na wykresie."""
    instructions.set("Wizualizacja trajektorii...")
    subprocess.run(["python", "tracking.py"])
    instructions.set("Wizualizacja zakończona.")


# GUI
root = tk.Tk()
root.title("GUI do analizy filmów i trajektorii")
root.geometry("600x400")

instructions = tk.StringVar()
instructions.set("Załaduj film, aby rozpocząć proces.")

label_instructions = tk.Label(root, textvariable=instructions, wraplength=500, justify="center")
label_instructions.pack(pady=20)

btn_trim = tk.Button(root, text="1. Podziel film na 30s fragmenty", command=trim_video, width=40)
btn_trim.pack(pady=5)

btn_extract = tk.Button(root, text="2. Podziel fragmenty na klatki", command=extract_frames, width=40)
btn_extract.pack(pady=5)

btn_detect = tk.Button(root, text="3. Uruchom detekcję YOLO", command=run_detection, width=40)
btn_detect.pack(pady=5)

btn_track = tk.Button(root, text="4. Uruchom tracker", command=run_tracker, width=40)
btn_track.pack(pady=5)

btn_visualize = tk.Button(root, text="5. Wizualizuj trajektorie", command=visualize_trajectories, width=40)
btn_visualize.pack(pady=5)

btn_exit = tk.Button(root, text="Zakończ", command=root.quit, width=40)
btn_exit.pack(pady=20)

root.mainloop()
