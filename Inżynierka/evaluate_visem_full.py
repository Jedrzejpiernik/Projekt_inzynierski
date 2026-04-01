import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import torch
import pandas as pd
import numpy as np
from sort.sort import Sort  # Upewnij się, że masz folder sort w projekcie
import warnings

warnings.filterwarnings("ignore")

VISEM_TRAIN_DIR = r"C:\Users\jszcz\PycharmProjects\inzynierkav1\VISEM_Tracking_Train_v4\Train"

MODEL_PATH = r"C:\Users\jszcz\PycharmProjects\inzynierkav1\best_checkpoints\yolov5l\weights\best.pt"

IMG_WIDTH = 640
IMG_HEIGHT = 480
VIDEO_FPS = 50
MY_FPS = 1
STEP = 50


def load_ground_truth(label_path):

    boxes = []
    if not os.path.exists(label_path):
        return boxes

    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()

            cls, xc, yc, w, h = map(float, parts)

            x1 = (xc - w / 2) * IMG_WIDTH
            y1 = (yc - h / 2) * IMG_HEIGHT
            x2 = (xc + w / 2) * IMG_WIDTH
            y2 = (yc + h / 2) * IMG_HEIGHT

            boxes.append([x1, y1, x2, y2])
    return np.array(boxes)


def calculate_iou(boxA, boxB):

    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    if float(boxAArea + boxBArea - interArea) == 0: return 0
    return interArea / float(boxAArea + boxBArea - interArea)


def evaluate_video(video_id, video_path):

    print(f"Przetwarzanie wideo ID: {video_id}...")


    model = torch.hub.load(r'C:\Users\jszcz\PycharmProjects\inzynierkav1\yolov5', 'custom', path=MODEL_PATH,
                           source='local')

    tracker = Sort()
    tp_total = 0
    fp_total = 0
    fn_total = 0
    images_path = os.path.join(video_path, "images")
    labels_path = os.path.join(video_path, "labels")
    frames = sorted([f for f in os.listdir(images_path) if f.endswith('.jpg') or f.endswith('.png')])


    for i in range(0, len(frames), STEP):
        frame_file = frames[i]
        img_path = os.path.join(images_path, frame_file)
        results = model(img_path)
        detections = results.xyxy[0].cpu().numpy()
        dets_to_sort = detections[:, :5]
        trackers = tracker.update(dets_to_sort)
        label_file = frame_file.replace('.jpg', '.txt').replace('.png', '.txt')
        gt_boxes = load_ground_truth(os.path.join(labels_path, label_file))
        matched_gt = set()

        for trk in trackers:
            pred_box = trk[:4]
            best_iou = 0
            best_gt_idx = -1

            for idx, gt in enumerate(gt_boxes):
                iou = calculate_iou(pred_box, gt)
                if iou > best_iou:
                    best_iou = iou
                    best_gt_idx = idx

            if best_iou >= 0.5:
                if best_gt_idx not in matched_gt:
                    tp_total += 1
                    matched_gt.add(best_gt_idx)
                else:
                    fp_total += 1
            else:
                fp_total += 1


        fn_total += (len(gt_boxes) - len(matched_gt))

    precision = tp_total / (tp_total + fp_total) if (tp_total + fp_total) > 0 else 0
    recall = tp_total / (tp_total + fn_total) if (tp_total + fn_total) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {'Video': video_id, 'Precision': round(precision, 3), 'Recall': round(recall, 3), 'F1': round(f1, 3)}


def main():
    all_results = []
    folders = [f for f in os.listdir(VISEM_TRAIN_DIR) if os.path.isdir(os.path.join(VISEM_TRAIN_DIR, f))]
    folders.sort(key=lambda x: int(x) if x.isdigit() else 0)

    print(f"Znaleziono {len(folders)} filmów do analizy.")

    for folder in folders:
        video_path = os.path.join(VISEM_TRAIN_DIR, folder)
        try:
            metrics = evaluate_video(folder, video_path)
            all_results.append(metrics)
            print(f"--> Wynik ID {folder}: P={metrics['Precision']}, R={metrics['Recall']}, F1={metrics['F1']}")
        except Exception as e:
            print(f"Błąd przy wideo {folder}: {e}")

    df = pd.DataFrame(all_results)
    print("\n=== WYNIKI ZBIORCZE ===")
    print(df)

    avg_p = df['Precision'].mean()
    avg_r = df['Recall'].mean()
    avg_f1 = df['F1'].mean()

    print(f"\nŚREDNIA: Precision={avg_p:.3f}, Recall={avg_r:.3f}, F1={avg_f1:.3f}")

    df.to_csv("wyniki_visem_full.csv", index=False)
    print("Zapisano do wyniki_visem_full.csv")


if __name__ == "__main__":
    main()