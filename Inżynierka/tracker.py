import pandas as pd
from sort.sort import Sort
import os

# Ścieżka do folderu runs/detect
detect_folder = "C:/Users/jszcz/PycharmProjects/inzynierkav1/yolov5/runs/detect"

# Znajdowanie najnowszego folderu exp
exp_folders = [os.path.join(detect_folder, d) for d in os.listdir(detect_folder) if d.startswith("exp")]
latest_exp = max(exp_folders, key=os.path.getmtime)

# Ŝieżka do najnowszego detections.csv
detections_csv_path = os.path.join(latest_exp, "detections.csv")

# Wczytanie danych
print(f"Używany plik: {detections_csv_path}")
df = pd.read_csv(detections_csv_path, header=None)

# Podgląd danych
print(df.head())

# Nazwij odpowiednie kolumny w DataFrame (upewnij się, że nazwy odpowiadają twojemu plikowi CSV)
df.columns = ['frame_number', 'x1', 'y1', 'x2', 'y2']

# Inicjalizacja SORT
tracker = Sort()

# Przygotowanie listy na wyniki
results = []

# Przetwarzanie danych klatka po klatce
for frame_id in sorted(df['frame_number'].unique()):  # Sortowanie ramek rosnąco
    frame_data = df[df['frame_number'] == frame_id]  # Filtruj dane dla bieżącej klatki

    # Wyciąganie bounding boxów (współrzędnych x1, y1, x2, y2)
    detections = frame_data[['x1', 'y1', 'x2', 'y2']].values

    # Aktualizacja trackera
    tracks = tracker.update(detections)

    # Zapisywanie wyników
    for track in tracks:
        x1, y1, x2, y2, track_id = track
        results.append([frame_id, int(track_id), x1, y1, x2, y2])

# Tworzenie DataFrame z wynikami
results_df = pd.DataFrame(results, columns=['frame_number', 'track_id', 'x1', 'y1', 'x2', 'y2'])

# Sortowanie wyników po numerze klatki
results_df = results_df.sort_values(by='frame_number').reset_index(drop=True)

# Ścieżka zapisu wyników
tracked_csv_path = "C:/Users/jszcz/PycharmProjects/inzynierkav1/tracked_sperm.csv"
if os.path.exists(tracked_csv_path):
    os.remove(tracked_csv_path)
# Zapis wyników do pliku CSV
results_df.to_csv(tracked_csv_path, index=False)

print(f"Wyniki śledzenia zapisano w pliku: {tracked_csv_path}")
