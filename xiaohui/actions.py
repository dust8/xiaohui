from datetime import datetime
import subprocess
import webbrowser

from .tts import utter_message
from .utils import lnk


class Action:
    def __init__(self, intent, slots):
        self.intent = intent
        self.slots = slots

        self.name = f"action_{intent}"

    def run(self):
        pass

    def __str__(self):
        return f"{self.intent} {self.slots}"


class ActionGreet(Action):
    def run(self):
        utter_message("您好,我叫小灰")


class ActionGoodbye(Action):
    def run(self):
        utter_message("再见")
        exit()


class ActionGet_time(Action):
    def run(self):
        utter_message(f'现在是{str(datetime.now()).split(".")[0]}')


class ActionOpen_program(Action):
    def run(self):
        programe_name = self.slots[0]["value"]
        programe_exe = lnk.PROGRAMS.get(programe_name)
        if programe_exe:
            subprocess.call([programe_exe])
        else:
            utter_message(f"未找到程序{programe_name}")


class ActionSearch(Action):
    def run(self):
        search = self.slots[0]["value"]
        url = f"https://www.baidu.com/s?ie=UTF-8&wd={search}"
        webbrowser.get().open(url)
