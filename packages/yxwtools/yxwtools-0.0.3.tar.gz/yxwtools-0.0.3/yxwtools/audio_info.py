import os
import librosa
import concurrent.futures
import matplotlib.pyplot as plt


def get_audio_duration(file_path):
    # 读取音频文件的时长
    return librosa.get_duration(filename=file_path)


def get_audio_duration_distribution(directory):
    durations = []
    total_duration = 0.0
    # 遍历目录下的所有文件
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 获取每个文件的时长
        durations = list(executor.map(get_audio_duration,
                                      [os.path.join(directory, filename) for filename in os.listdir(directory) if
                                       filename.endswith('.wav')]))
    total_duration = sum(durations)

    # 统计时长分布
    duration_counts = {}
    for duration in durations:
        duration = round(duration, 2)  # 四舍五入保留两位小数
        if duration in duration_counts:
            duration_counts[duration] += 1
        else:
            duration_counts[duration] = 1

    return total_duration, duration_counts



def get_audio_info(directory):
    # 获取时长分布和总时长
    total_duration, duration_counts = get_audio_duration_distribution(directory)

    # 输出总时长
    print(f'Total duration of audio files: {total_duration} seconds')
    print(f'Total duration of audio files: {total_duration / 3600} hours')

    # 绘制时长分布图
    plt.figure(figsize=(12, 6))
    plt.bar(duration_counts.keys(), duration_counts.values())
    plt.xlabel('Duration (seconds)')
    plt.ylabel('Count')
    plt.title('Audio Duration Distribution')
    plt.show()

