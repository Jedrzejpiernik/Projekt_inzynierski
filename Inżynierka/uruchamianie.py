import os

# Ścieżka do folderu z modelami
base_path = "best_checkpoints"
models = ["yolov5l"]

for model in models:
    weights_path = os.path.join(base_path, model, "weights", "best.pt")
    command = f"python C:/Users/jszcz/PycharmProjects/inzynierkav1/yolov5/detect.py --weights {weights_path} --source C:/Users/jszcz/PycharmProjects/inzynierkav1/yolov5/data/images --save-csv"
    print(f"Uruchamianie dla modelu: {model}, komenda: {command}")

    os.system(command)
