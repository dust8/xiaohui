"""
TTS 指的是语音合成
"""
import tempfile

from gtts import gTTS
import gtts_token
from playsound import playsound

from .utils import hotfix

gtts_token.gtts_token.Token._get_token_key = hotfix._get_token_key


def utter_message(audio_string):
    print(audio_string)
    tts = gTTS(audio_string, tld="cn", lang="zh-cn")

    audio_file = tempfile.NamedTemporaryFile(mode="wb", suffix=".mp3", delete=False)
    audio_file_name = audio_file.name
    tts.save(audio_file_name)
    audio_file.close()

    playsound(audio_file_name)

