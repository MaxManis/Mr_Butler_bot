import config_files.config as config
import speech_recognition as sr
import os
from subprocess import Popen
import time
import random


def speech_rec(input_audio, user_id=random.randint(46, 24357)):
    try:
        new_path = f'{config.voice_wav_abs_path}WAV_file-{user_id}-{random.randint(146, 24357)}.wav'
        args = ['ffmpeg', '-i', input_audio, new_path]
        Popen(executable=f"{config.ffmpeg_path}ffmpeg.exe", args=args)
        # new_1_path = f'../files/voice_rec/new_file-{user_id}.wav'
        time.sleep(5)
        r = sr.Recognizer()
        harvard = sr.AudioFile(new_path)
        with harvard as source:
            audio = r.record(source)

        res = r.recognize_google(audio, language='ru-RU')  # ['ru-RU', 'en-US', 'uk-UA']
        os.remove(input_audio)
        os.remove(new_path)
    except:
        res = 'Не удалось распознать =('
        os.remove(input_audio)
    print(res)
    return str(res)
