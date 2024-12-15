import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# Wczytaj dane
csv_path = "C:/Users/jszcz/PycharmProjects/inzynierkav1/tracked_sperm.csv"
df = pd.read_csv(csv_path)


# Funkcja pomocnicza - obliczenie centrum dla każdego obiektu
def calculate_center(df):
    df['x_center'] = (df['x1'] + df['x2']) / 2
    df['y_center'] = (df['y1'] + df['y2']) / 2
    return df


df = calculate_center(df)

# Grupa ramek po numerze klatki (frame)
frames = df['frame_number'].unique()

# Przygotowanie wykresu
fig, ax = plt.subplots()
scatter = ax.scatter([], [], c='red', label='Plemniki')  # Punkty
arrows = []  # Strzałki dla ruchu
title = ax.text(0.5, 1.05, "", ha="center", transform=ax.transAxes, fontsize=12)


# Funkcja aktualizacji wykresu dla każdej klatki
def update(frame_number):
    global arrows
    ax.clear()  # Czyść poprzednią klatkę

    # Pobierz dane dla aktualnej i poprzedniej klatki
    current_frame = df[df['frame_number'] == frame_number]
    prev_frame = df[df['frame_number'] == frame_number - 1] if frame_number > 0 else None

    # Rysowanie aktualnych punktów
    ax.scatter(current_frame['x_center'], current_frame['y_center'], c='red', label='Plemniki')

    # Dodanie strzałek pokazujących ruch plemników na podstawie track_id
    if prev_frame is not None:
        for _, row in current_frame.iterrows():
            prev_row = prev_frame[prev_frame['track_id'] == row['track_id']]
            if not prev_row.empty:
                ax.arrow(prev_row['x_center'].values[0], prev_row['y_center'].values[0],
                         row['x_center'] - prev_row['x_center'].values[0],
                         row['y_center'] - prev_row['y_center'].values[0],
                         head_width=5, head_length=5, fc='blue', ec='blue')
    sperm_count = len(current_frame)
    ax.set_title(f"Klatka: {frame_number} | Liczba plemników: {sperm_count}", fontsize=14)
    # Ustawienia osi i tytułu
    ax.set_xlim(0, df['x_center'].max() + 10)
    ax.set_ylim(0, df['y_center'].max() + 10)
    title.set_text(f"Klatka: {frame_number}")



# Funkcja animacji
ani = FuncAnimation(fig, update, frames=frames, interval=1000, repeat=False)

# Wyświetlanie wykresu
plt.legend()
plt.show()
