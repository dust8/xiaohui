"""
ASR 指的是自动语音识别
"""
import speech_recognition as sr

from .utils import hotfix

sr.Recognizer.recognize_google = hotfix.recognize_google
r = sr.Recognizer()


def record_audio():
    with sr.Microphone() as source:
        voice_data = ""
        try:
            # audio = r.listen(source)
            audio = r.listen(source, timeout=20, phrase_time_limit=5)
            voice_data = r.recognize_google(audio, language="zh-CN")
        except sr.WaitTimeoutError:
            print("超时")
        except sr.UnknownValueError:
            print("小灰没听懂")
        except sr.RequestError:
            print("连接中断")

        return voice_data
