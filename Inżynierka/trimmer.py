import os
import subprocess
from datetime import timedelta
import re


def get_length(input_video):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
         input_video],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    length = float(result.stdout)
    print(f"Długość wideo: {length} sekund")  # Dodaj to
    return length


def clear_folder(folder_path):
    """
    Usuwa wszystkie pliki z podanego katalogu.
    """
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Usunięcie pliku
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)  # Usunięcie katalogu
            except Exception as e:
                print(f'Błąd przy usuwaniu {file_path}. Powód: {e}')


def sanitize_filename(filename):
    """
    Normalizuje nazwę pliku - usuwa spacje i nieprawidłowe znaki.
    """
    filename = re.sub(r'[^\w\._-]', '_', filename)  # Zamienia nieprawidłowe znaki na podkreślenie
    return filename


def trim_videos(input_dir, output_dir):
    """
    Dzieli filmy w katalogu wejściowym na 30-sekundowe fragmenty.
    """
    CHUNK_SIZE = 30  # Długość fragmentu w sekundach
    os.makedirs(output_dir, exist_ok=True)  # Tworzy katalog wyjściowy, jeśli nie istnieje

    # Czyszczenie katalogu wyjściowego przed zapisem nowych plików
    print("Czyszczenie katalogu wyjściowego...")
    clear_folder(output_dir)

    # Lista wszystkich plików w katalogu wejściowym
    v_files = os.listdir(input_dir)

    for v_file in v_files:
        if v_file.endswith(".mp4"):  # Obsługuje tylko pliki MP4
            input_file = os.path.join(input_dir, v_file)
            v_file_id = v_file.split(".")[0]  # Nazwa pliku bez rozszerzenia
            sanitized_file_id = sanitize_filename(v_file_id)  # Oczyszczona nazwa
            total_time_s = get_length(input_file)

            # Dzieli film na 30-sekundowe fragmenty
            for tt in range(0, int(total_time_s), CHUNK_SIZE):
                trim_start = tt
                trim_stop = tt + CHUNK_SIZE

                output_path = os.path.join(output_dir, f'{sanitized_file_id}_{trim_start}_{trim_stop}.mp4')
                trim_start_hh_mm_ss = str(timedelta(seconds=trim_start))
                chunk_size_hh_mm_ss = str(timedelta(seconds=CHUNK_SIZE))

                # Komenda ffmpeg do dzielenia filmu
                cmd = f'ffmpeg -i "{input_file}" -ss {trim_start_hh_mm_ss} -t {chunk_size_hh_mm_ss} -c:v libx264 "{output_path}"'
                subprocess.run(cmd, shell=True)
                print(f"Zapisano: {output_path}")

    print("Dzielenie filmów zakończone.")



if __name__ == "__main__":
    # Ścieżki domyślne
    default_input_dir = "C:/Users/jszcz/PycharmProjects/inzynierkav1/videos"
    default_output_dir = "C:/Users/jszcz/PycharmProjects/inzynierkav1/trimmed_videos"

    # Pobranie ścieżek lub użycie domyślnych
    input_dir = input("Podaj katalog wejściowy (ENTER dla domyślnego): ").strip()
    output_dir = input("Podaj katalog wyjściowy (ENTER dla domyślnego): ").strip()

    if not input_dir:
        input_dir = default_input_dir
    if not output_dir:
        output_dir = default_output_dir

    # Sprawdzenie czy katalog wejściowy istnieje
    if not os.path.exists(input_dir):
        print(f"Podany katalog wejściowy nie istnieje: {input_dir}")
    else:
        trim_videos(input_dir, output_dir)
