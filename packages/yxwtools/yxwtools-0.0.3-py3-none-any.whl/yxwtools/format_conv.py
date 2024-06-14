'''
将flac mp3音频转换为wav音频
'''
import os
from pydub import AudioSegment


def convert_flac_to_wav(input_dir, output_dir):
    # 检查并创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录下的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith(".flac"):
            flac_file_path = os.path.join(input_dir, filename)
            wav_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".wav")

            # 读取FLAC文件并转换为WAV文件
            audio = AudioSegment.from_file(flac_file_path, format="flac")
            audio.export(wav_file_path, format="wav")

            print(f"Converted {flac_file_path} to {wav_file_path}")


def convert_mp3_to_wav(input_dir, output_dir):
    # 检查并创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录下的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith(".mp3"):
            flac_file_path = os.path.join(input_dir, filename)
            wav_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".wav")

            # 读取FLAC文件并转换为WAV文件
            audio = AudioSegment.from_file(flac_file_path, format="mp3")
            audio.export(wav_file_path, format="wav")

            print(f"Converted {flac_file_path} to {wav_file_path}")

# 示例使用
# input_directory = "./mp3"
# output_directory = "./wav3"
# convert_mp3_to_wav(input_directory, output_directory)
#
# print("All FLAC files have been converted to WAV format.")
