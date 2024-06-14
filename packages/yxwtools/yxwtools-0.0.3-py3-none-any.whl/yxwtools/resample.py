'''
重采样
'''
from pydub import AudioSegment
import sys
import torchaudio
import os

def wavresample(wavfile,sr=16000):
    '''
    输入wav文件目录和目标采样率
    该函数生成对应的音频文件，并直接替换掉源文件
    '''
    # 读取音频文件
    audio = AudioSegment.from_wav(wavfile)
    # 将音频重采样到16000Hz并转换为单声道
    resampled_audio = audio.set_frame_rate(sr).set_channels(1)

    # 导出处理后的音频文件
    resampled_audio.export(wavfile, format='wav')

def wavresample_torch(wavfile,sr=16000):
    '''
    输入wav文件目录和目标采样率
    该函数生成对应的音频文件，并直接替换掉源文件
    使用torchaudio的接口进行重采样
    '''
    waveform, sample_rate = torchaudio.load(wavfile)

    # 将音频重采样到16000Hz并转换为单声道
    resampled_waveform = torchaudio.transforms.Resample(sample_rate, sr)(waveform)
    resampled_waveform = resampled_waveform.mean(dim=0, keepdim=True)

    # 导出处理后的音频文件
    torchaudio.save(wavfile, resampled_waveform, sr)

def wavdir_resample(wavdir,sr,is_torch=False):
    '''
    :param wavdir: 待重采样的文件夹
    :param sr: 目标采样率
    :param is_torch: 是否使用torchaudio的接口进行重采样
    :return: 将目标文件夹内的所有wav文件进行重采样
    '''
    for filename in os.listdir(wavdir):
        if filename.endswith('.wav'):
            input_path = os.path.join(input_dir, filename)
            if is_torch:
                wavresample_torch(input_path,sr)
            else:
                wavresample(input_path,sr)




if __name__ =="__main__":
    wavresample(sys.argv[1])

