import os
from klatki import extract_frames


def test_extract_frames():
    # Przygotowanie
    test_video = "C:/Users/jszcz/PycharmProjects/inzynierkav1/trimmed_videos/24_0_30.mp4"
    output_dir = "C:/Users/jszcz/PycharmProjects/inzynierkav1/yolov5/data/images"

    os.makedirs(output_dir, exist_ok=True)  # Tworzymy folder wyjściowy

    # Symulacja działania funkcji
    try:
        extract_frames(test_video, output_dir)
        extracted_files = os.listdir(output_dir)

        # Sprawdzamy, czy klatki zostały zapisane
        assert len(extracted_files) > 0, "Brak wygenerowanych klatek w folderze"
        print(f"Test passed: Wyodrębniono {len(extracted_files)} klatek.")
    finally:
        # Usuwamy utworzone pliki
        for f in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, f))
        os.rmdir(output_dir)


if __name__ == "__main__":
    test_extract_frames()
