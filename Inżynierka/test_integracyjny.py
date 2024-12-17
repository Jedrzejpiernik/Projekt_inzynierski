import os
import pandas as pd
import numpy as np
from trimmer import trim_videos
from klatki import extract_frames
from tracker import tracker

def test_integration_pipeline():
    # Ścieżki
    input_video = "C:/Users/jszcz/PycharmProjects/inzynierkav1/videos"
    trimmed_output = "C:/Users/jszcz/PycharmProjects/inzynierkav1/trimmed_videos"
    frames_output = r"C:\Users\jszcz\PycharmProjects\inzynierkav1\yolov5\data\images"
    tracked_output = "C:/Users/jszcz/PycharmProjects/inzynierkav1/tracked_sperm.csv"

    # 1. Podział wideo na fragmenty
    os.makedirs(trimmed_output, exist_ok=True)
    trim_videos(input_video, trimmed_output)
    assert len(os.listdir(trimmed_output)) > 0, "Brak podzielonych fragmentów wideo"

    # 2. Wyodrębnianie klatek z pierwszego fragmentu
    fragment_path = os.path.join(trimmed_output, os.listdir(trimmed_output)[0])
    os.makedirs(frames_output, exist_ok=True)
    extract_frames(fragment_path, frames_output)
    assert len(os.listdir(frames_output)) > 0, "Brak wygenerowanych klatek"

    # 3. Przygotowanie przykładowych detekcji dla trackera
    fake_detections = np.array([[50, 50, 100, 100]])  # Przykładowy bounding box: x1, y1, x2, y2

    # 4. Uruchomienie trackera
    tracker.update(fake_detections)
    assert os.path.exists(tracked_output), "Brak pliku wynikowego z trackerem"

    # 5. Sprawdzenie poprawności pliku CSV
    df = pd.read_csv(tracked_output)
    assert 'frame_number' in df.columns, "Brak kolumny 'frame_number'"
    assert 'track_id' in df.columns, "Brak kolumny 'track_id'"
    print("Test integracyjny przeszedł pomyślnie!")

    # Sprzątanie (opcjonalne)
    for folder in [trimmed_output, frames_output]:
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))
        os.rmdir(folder)
    os.remove(tracked_output)


if __name__ == "__main__":
    test_integration_pipeline()
