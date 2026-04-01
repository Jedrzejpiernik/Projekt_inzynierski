import subprocess
import os
#import ffmpeg


input_dir = "C:/Users/jszcz/PycharmProjects/inzynierkav1/videos"
output_dir = "C:/Users/jszcz/PycharmProjects/inzynierkav1/segmentyvideo"

os.makedirs(output_dir,exist_ok=True)

v_files = os.listdir(input_dir)

for v_file in v_files:
    v_file_id = v_file.split(".")[0]
    print(v_file_id)
    input_file = os.path.join(input_dir, v_file)
    output_path = os.path.join(output_dir, f'{v_file_id}.mp4')

    cmd = f'ffmpeg -i {input_file} -ss 00:00:00 -t 00:00:30 -c:v libx264 {output_path}'
    print("CMD RUNNING=", cmd)
    subprocess.run(str(cmd), shell=True)


    #ffmpeg -i videos/623.mkv -ss 00:00:00 -t 00:00:30 -c:v libx264 output3.mp4