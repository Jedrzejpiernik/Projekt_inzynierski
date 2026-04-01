import pandas as pd
import matplotlib.pyplot as plt
import os


CSV_PATH = r"C:\Users\jszcz\PycharmProjects\inzynierkav1\tracked_sperm.csv"


def plot_trajectories():

    if not os.path.exists(CSV_PATH):
        print(f"BŁĄD: Nie znaleziono pliku {CSV_PATH}")
        return
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        print(f"Błąd odczytu pliku CSV: {e}")
        return

    if df.empty:
        print("Plik CSV jest pusty.")
        return
    df['x'] = (df['x1'] + df['x2']) / 2
    df['y'] = (df['y1'] + df['y2']) / 2
    plt.figure(figsize=(12, 10))
    plt.title("Wizualizacja Trajektorii Plemników (Po korekcie)", fontsize=16)
    track_ids = df['track_id'].unique()
    print(f"Znaleziono {len(track_ids)} unikalnych ścieżek.")

    for tid in track_ids:
        track = df[df['track_id'] == tid]
        track = track.sort_values(by='frame_number')
        plt.plot(track['x'], track['y'], linewidth=2, marker='.', markersize=3, alpha=0.7, label=f"ID {int(tid)}")
        if not track.empty:
            start_x = track.iloc[0]['x']
            start_y = track.iloc[0]['y']
            plt.text(start_x, start_y, str(int(tid)), fontsize=8, color='black', fontweight='bold')
    plt.xlabel("Pozycja X (piksele)")
    plt.ylabel("Pozycja Y (piksele)")
    plt.gca().invert_yaxis()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.axis('equal')
    print("Wyświetlanie wykresu...")
    plt.show()

if __name__ == "__main__":
    plot_trajectories()