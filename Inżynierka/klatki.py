import os
import cv2
import shutil
import re
from tkinter import Tk, filedialog


def clear_folder(folder_path):
    """Usuwa wszystkie pliki i podfoldery z podanego folderu."""
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
    else:
        os.makedirs(folder_path)
    print(f"Folder {folder_path} został wyczyszczony.")


def sanitize_filename(filename):
    """Normalizuje nazwę pliku - usuwa spacje i nieprawidłowe znaki."""
    filename = re.sub(r'[^\w\._-]', '_', filename)
    return filename


def extract_frames(video_path, output_dir):
    """Ekstrakcja dokładnie jednej klatki na sekundę."""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    print(f"Długość filmu: {duration} sekund | FPS: {fps}")

    already_saved = set()
    os.makedirs(output_dir, exist_ok=True)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Czas w sekundach
        if int(current_time) not in already_saved:
            already_saved.add(int(current_time))
            frame_path = os.path.join(output_dir, f"frame_{int(current_time)}.jpg")
            cv2.imwrite(frame_path, frame)
            print(f"Zapisano klatkę: {frame_path}")

    cap.release()
    print("Wyodrębnianie klatek zakończone.")


    cap.release()
    print("Wyodrębnianie klatek zakończone.")


if __name__ == "__main__":
    # Tworzymy okno dialogowe do wyboru pliku
    Tk().withdraw()  # Ukrywa główne okno tkinter
    video_path = filedialog.askopenfilename(
        title="Wybierz plik wideo do podziału na klatki",
        filetypes=[("Pliki MP4", "*.mp4")],
        initialdir="C:/Users/jszcz/PycharmProjects/inzynierkav1/trimmed_videos"
    )

    if not video_path:
        print("Nie wybrano pliku. Operacja anulowana.")
    else:
        print(f"Wybrano plik: {video_path}")
        output_dir = r"C:\Users\jszcz\PycharmProjects\inzynierkav1\yolov5\data\images"
        frame_interval = 30  # Podział co sekundę
        extract_frames(video_path, output_dir)
