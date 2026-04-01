import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import os

CSV_PATH = r"C:\Users\jszcz\PycharmProjects\inzynierkav1\tracked_sperm.csv"


def visualize_probable_path(track_id_to_plot=None):
    if not os.path.exists(CSV_PATH):
        print("Brak pliku CSV!")
        return

    df = pd.read_csv(CSV_PATH)


    df['x'] = (df['x1'] + df['x2']) / 2
    df['y'] = (df['y1'] + df['y2']) / 2

    if track_id_to_plot is None:
        track_counts = df['track_id'].value_counts()
        if track_counts.empty:
            print("Brak danych w pliku.")
            return
        track_id_to_plot = track_counts.idxmax()
        print(f"Automatycznie wybrano najdłuższą ścieżkę: ID {track_id_to_plot}")

    track = df[df['track_id'] == track_id_to_plot].sort_values(by='frame_number')

    if len(track) < 4:
        print("Za mało punktów do wygładzania (minimum 4).")
        return

    x = track['x'].to_numpy()
    y = track['y'].to_numpy()

    X_Y_Spline = make_interp_spline(np.arange(len(x)), np.c_[x, y], k=3)

    X_new = np.linspace(0, len(x) - 1, 500)
    X_Y_smooth = X_Y_Spline(X_new)
    x_smooth, y_smooth = X_Y_smooth[:, 0], X_Y_smooth[:, 1]

    plt.figure(figsize=(10, 8))
    plt.plot(x, y, 'o', color='red', label='Detekcje (Pomiary 1 FPS)', zorder=3)
    plt.plot(x, y, '--', color='gray', alpha=0.5, label='Surowa trajektoria (Liniowa)', zorder=2)
    plt.plot(x_smooth, y_smooth, '-', color='blue', linewidth=3, alpha=0.8,
             label='Estymowany ruch biologiczny (Wygładzony)', zorder=1)

    plt.title(f"Rekonstrukcja ruchu plemnika (ID: {track_id_to_plot})", fontsize=14)
    plt.xlabel("Pozycja X (px)")
    plt.ylabel("Pozycja Y (px)")
    plt.gca().invert_yaxis()  # Odwrócenie osi Y (dla obrazów)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)

    output_file = "rekonstrukcja_ruchu.png"
    plt.savefig(output_file, dpi=300)
    print(f"Wykres zapisano jako {output_file}")
    plt.show()


if __name__ == "__main__":
    visualize_probable_path(108)