import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import matplotlib.image as mpimg
import os
import numpy as np

CSV_PATH = r"C:\Users\jszcz\PycharmProjects\inzynierkav1\tracked_sperm.csv"
IMAGES_DIR = r"C:\Users\jszcz\PycharmProjects\inzynierkav1\yolov5\data\images"

if not os.path.exists(CSV_PATH):
    print(f"BŁĄD: Nie znaleziono pliku CSV: {CSV_PATH}")
    df = pd.DataFrame(columns=['frame_number', 'track_id', 'x1', 'y1', 'x2', 'y2'])
else:
    df = pd.read_csv(CSV_PATH)

if not df.empty:
    df['x_center'] = (df['x1'] + df['x2']) / 2
    df['y_center'] = (df['y1'] + df['y2']) / 2
    df = df.sort_values(by=['frame_number', 'track_id'])
    frames = sorted(list(df['frame_number'].unique()))
else:
    frames = []
    print("UWAGA: Plik CSV jest pusty.")

current_frame_index = 0
is_paused = True
current_hovered_track_id = None
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 7))
plt.subplots_adjust(bottom=0.2)

crosshair_v = ax2.axvline(x=0, color='lime', linestyle='--', linewidth=1, alpha=0)
crosshair_h = ax2.axhline(y=0, color='lime', linestyle='--', linewidth=1, alpha=0)
highlight_point_1, = ax1.plot([], [], 'o', color='yellow', markeredgecolor='black', markersize=12, zorder=10)
highlight_point_3, = ax3.plot([], [], 'o', color='yellow', markeredgecolor='black', markersize=12, zorder=10)
scatter_tracker = None
scatter_overlay = None


def get_raw_image_path(frame_number):
    filename = f"frame_{int(frame_number)}.jpg"
    return os.path.join(IMAGES_DIR, filename)


def update_plot(frame_idx):
    global scatter_tracker, scatter_overlay, crosshair_v, crosshair_h
    global highlight_point_1, highlight_point_3

    if not frames:
        ax1.clear();
        ax2.clear();
        ax3.clear()
        ax1.text(0.5, 0.5, "BRAK DANYCH", ha='center')
        return

    if frame_idx >= len(frames): frame_idx = 0
    frame_number = frames[frame_idx]
    current_data = df[df['frame_number'] == frame_number]
    img_path = get_raw_image_path(frame_number)
    raw_img = None
    img_h, img_w = 640, 640

    if os.path.exists(img_path):
        raw_img = mpimg.imread(img_path)
        img_h, img_w = raw_img.shape[:2]

    ax1.clear()
    ax1.set_title(f"1. Tracker (Sekunda: {frame_number})")
    ax1.set_xlim(0, img_w)
    ax1.set_ylim(img_h, 0)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)

    scatter_tracker = ax1.scatter(
        current_data['x_center'],
        current_data['y_center'],
        c='blue', label='Obiekty', picker=5
    )

    ax1.add_artist(highlight_point_1)

    ax2.clear()
    ax2.set_title("2. Surowa klatka (bez detekcji)")
    if raw_img is not None:
        ax2.imshow(raw_img)
    else:
        ax2.text(img_w / 2, img_h / 2, "Brak pliku obrazu!", ha='center')

    ax2.set_xlim(0, img_w)
    ax2.set_ylim(img_h, 0)
    ax2.set_aspect('equal')

    ax2.add_artist(crosshair_v)
    ax2.add_artist(crosshair_h)

    ax3.clear()
    ax3.set_title("3. Weryfikacja (Obraz + Tracker)")
    if raw_img is not None:
        ax3.imshow(raw_img)

    ax3.set_xlim(0, img_w)
    ax3.set_ylim(img_h, 0)
    ax3.set_aspect('equal')

    scatter_overlay = ax3.scatter(
        current_data['x_center'],
        current_data['y_center'],
        c='red', s=20, marker='x', picker=5
    )

    ax3.add_artist(highlight_point_3)
    fig.canvas.draw_idle()
def on_mouse_move(event):
    global current_hovered_track_id

    if event.inaxes == ax1:
        x, y = event.xdata, event.ydata

        if x is None or y is None: return
        crosshair_v.set_xdata([x])
        crosshair_h.set_ydata([y])
        crosshair_v.set_alpha(1.0)
        crosshair_h.set_alpha(1.0)

        if not frames: return
        frame_number = frames[current_frame_index]
        current_data = df[df['frame_number'] == frame_number]

        if not current_data.empty:
            distances = np.sqrt((current_data['x_center'] - x) ** 2 + (current_data['y_center'] - y) ** 2)
            min_dist_idx = distances.idxmin()
            min_dist = distances.min()

            if min_dist < 20:
                point = current_data.loc[min_dist_idx]
                px, py = point['x_center'], point['y_center']
                current_hovered_track_id = point['track_id']
                highlight_point_1.set_data([px], [py])
                highlight_point_3.set_data([px], [py])

                ax1.set_title(f"Tracker (ID: {int(current_hovered_track_id)}) - Kliknij by usunąć z CAŁEGO FILMU",
                              color='red', fontweight='bold')
            else:
                highlight_point_1.set_data([], [])
                highlight_point_3.set_data([], [])
                current_hovered_track_id = None
                ax1.set_title(f"1. Tracker (Sekunda: {frame_number})", color='black')

        fig.canvas.draw_idle()


def on_click_remove(event):
    global df, frames, current_frame_index

    if event.artist not in [scatter_tracker, scatter_overlay]:
        return

    ind = event.ind
    if len(ind) == 0: return

    frame_number = frames[current_frame_index]
    current_data_slice = df[df['frame_number'] == frame_number]
    point_row = current_data_slice.iloc[ind[0]]
    track_id_to_remove = point_row['track_id']
    print(f"!!! USUWANIE !!! Kliknięto ID: {track_id_to_remove}")

    original_count = len(df)
    df = df[df['track_id'] != track_id_to_remove]
    removed_count = original_count - len(df)
    print(f"Usunięto obiekt ID {track_id_to_remove} z całego filmu (łącznie {removed_count} klatek).")
    highlight_point_1.set_data([], [])
    highlight_point_3.set_data([], [])
    update_plot(current_frame_index)


fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)
fig.canvas.mpl_connect('pick_event', on_click_remove)

ax_prev = plt.axes([0.1, 0.05, 0.1, 0.075])
ax_play = plt.axes([0.21, 0.05, 0.1, 0.075])
ax_next = plt.axes([0.32, 0.05, 0.1, 0.075])
ax_save = plt.axes([0.43, 0.05, 0.15, 0.075])

btn_prev = Button(ax_prev, 'Poprzednia')
btn_play = Button(ax_play, 'Start/Stop')
btn_next = Button(ax_next, 'Następna')
btn_save = Button(ax_save, 'Zapisz Plik')


def prev_f(event):
    global current_frame_index
    if current_frame_index > 0:
        current_frame_index -= 1
        update_plot(current_frame_index)


def next_f(event):
    global current_frame_index
    if current_frame_index < len(frames) - 1:
        current_frame_index += 1
        update_plot(current_frame_index)


def play_f(event):
    global is_paused
    is_paused = not is_paused


def save_f(event):
    try:
        df.to_csv(CSV_PATH, index=False)
        print(f"ZAPISANO PLIK: {CSV_PATH}")
        ax1.set_title("ZAPISANO ZMIANY!", color='green', fontweight='bold')
        fig.canvas.draw_idle()
    except Exception as e:
        print(f"BŁĄD ZAPISU: {e}")


btn_prev.on_clicked(prev_f)
btn_next.on_clicked(next_f)
btn_play.on_clicked(play_f)
btn_save.on_clicked(save_f)


def animation_loop(frame):
    if not is_paused and frames:
        global current_frame_index
        current_frame_index = (current_frame_index + 1) % len(frames)
        update_plot(current_frame_index)


# Start
if frames:
    update_plot(0)
    ani = FuncAnimation(fig, animation_loop, interval=1000, save_count=50)
    plt.show()
else:
    print("Brak danych do wyświetlenia.")