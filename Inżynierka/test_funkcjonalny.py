import os
import subprocess
import pandas as pd

def test_functional_pipeline():
    # Ścieżki
    input_video = "C:/Users/jszcz/PycharmProjects/inzynierkav1/videos"
    tracked_output = "C:/Users/jszcz/PycharmProjects/inzynierkav1/tracked_sperm.csv"

    # 1. Uruchomienie podziału wideo
    result = subprocess.run(["python", "trimmer.py"], capture_output=True)
    assert result.returncode == 0, "Błąd podczas podziału wideo"

    # 2. Uruchomienie wyodrębniania klatek
    result = subprocess.run(["python", "klatki.py"], capture_output=True)
    assert result.returncode == 0, "Błąd podczas wyodrębniania klatek"

    # 3. Uruchomienie trackera
    result = subprocess.run(["python", "tracker.py"], capture_output=True)
    assert result.returncode == 0, "Błąd podczas śledzenia obiektów"

    # 4. Sprawdzenie pliku CSV
    assert os.path.exists(tracked_output), "Brak pliku wynikowego CSV"
    df = pd.read_csv(tracked_output)
    assert len(df) > 0, "Plik wynikowy jest pusty"
    print("Test funkcjonalny zakończony sukcesem!")

if __name__ == "__main__":
    test_functional_pipeline()
