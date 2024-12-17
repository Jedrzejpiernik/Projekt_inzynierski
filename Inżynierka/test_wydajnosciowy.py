import time
import os
import numpy as np
import cv2
from trimmer import trim_videos
from klatki import extract_frames
from tracker import tracker


def test_performance():
    # Ścieżki do katalogów
    input_video = "C:/Users/jszcz/PycharmProjects/inzynierkav1/videos"
    trimmed_output = "C:/Users/jszcz/PycharmProjects/inzynierkav1/trimmed_videos"
    frames_output = r"C:\Users\jszcz\PycharmProjects\inzynierkav1\yolov5\data\images"

    # 1. Test wydajności podziału wideo
    os.makedirs(trimmed_output, exist_ok=True)
    print("\n--- Rozpoczęcie testu podziału wideo ---")
    start_time = time.time()
    trim_videos(input_video, trimmed_output)
    duration_trim = time.time() - start_time
    print(f"Podział wideo zakończony w {duration_trim:.2f} sekund.")

    # Sprawdzenie wyników podziału
    fragments = os.listdir(trimmed_output)
    assert len(fragments) > 0, "Błąd: Brak fragmentów w katalogu trimmed_videos!"
    print(f"Wygenerowano {len(fragments)} fragmentów wideo.")

    # 2. Test wydajności wyodrębniania klatek
    fragment_path = os.path.join(trimmed_output, fragments[0])  # Pierwszy fragment wideo
    os.makedirs(frames_output, exist_ok=True)
    print("\n--- Rozpoczęcie testu wyodrębniania klatek ---")

    # Sprawdzenie, czy plik wideo można otworzyć
    cap = cv2.VideoCapture(fragment_path)
    assert cap.isOpened(), f"Nie można otworzyć pliku wideo: {fragment_path}"
    cap.release()

    start_time = time.time()
    extract_frames(fragment_path, frames_output)
    duration_frames = time.time() - start_time
    print(f"Wyodrębnianie klatek zakończone w {duration_frames:.2f} sekund.")

    # Sprawdzenie wyników klatek
    frames = os.listdir(frames_output)
    assert len(frames) > 0, "Błąd: Brak wygenerowanych klatek!"
    print(f"Wygenerowano {len(frames)} klatek.")

    # 3. Test wydajności trackera
    print("\n--- Rozpoczęcie testu śledzenia obiektów ---")
    start_time = time.time()
    for _ in range(len(frames)):  # Symulacja przetwarzania dla każdej klatki
        fake_detections = np.random.randint(0, 500, size=(10, 4))  # 10 losowych bounding boxów
        tracker.update(fake_detections)
    duration_tracker = time.time() - start_time
    print(f"Śledzenie obiektów zakończone w {duration_tracker:.2f} sekund.")

    # Podsumowanie wyników
    print("\n--- Podsumowanie testu wydajnościowego ---")
    print(f"Podział wideo: {duration_trim:.2f} sekund.")
    print(f"Wyodrębnianie klatek: {duration_frames:.2f} sekund.")
    print(f"Śledzenie obiektów: {duration_tracker:.2f} sekund.")

    # Sprzątanie (opcjonalne)
    for folder in [trimmed_output, frames_output]:
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))
        os.rmdir(folder)


if __name__ == "__main__":
    test_performance()
