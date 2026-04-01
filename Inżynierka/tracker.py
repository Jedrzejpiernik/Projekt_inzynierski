import pandas as pd
from sort.sort import Sort
import os


detect_folder = "C:/Users/jszcz/PycharmProjects/inzynierkav1/yolov5/runs/detect"

exp_folders = [os.path.join(detect_folder, d) for d in os.listdir(detect_folder) if d.startswith("exp")]
latest_exp = max(exp_folders, key=os.path.getmtime)

detections_csv_path = os.path.join(latest_exp, "detections.csv")

print(f"Używany plik: {detections_csv_path}")
df = pd.read_csv(detections_csv_path, header=None)

print(df.head())

df.columns = ['frame_number', 'x1', 'y1', 'x2', 'y2']
tracker = Sort()
results = []

for frame_id in sorted(df['frame_number'].unique()):
    frame_data = df[df['frame_number'] == frame_id]
    detections = frame_data[['x1', 'y1', 'x2', 'y2']].values
    tracks = tracker.update(detections)
    for track in tracks:
        x1, y1, x2, y2, track_id = track
        results.append([frame_id, int(track_id), x1, y1, x2, y2])

results_df = pd.DataFrame(results, columns=['frame_number', 'track_id', 'x1', 'y1', 'x2', 'y2'])

results_df = results_df.sort_values(by='frame_number').reset_index(drop=True)

tracked_csv_path = "C:/Users/jszcz/PycharmProjects/inzynierkav1/tracked_sperm.csv"
if os.path.exists(tracked_csv_path):
    os.remove(tracked_csv_path)
results_df.to_csv(tracked_csv_path, index=False)

print(f"Wyniki śledzenia zapisano w pliku: {tracked_csv_path}")
