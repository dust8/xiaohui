import time

from . import actions
from .asr import record_audio
from .nlg import reply
from .nlu import intent_recognize
from .tts import utter_message


def main():
    utter_message("您好,小灰在这")

    while True:
        sentence = record_audio()
        if not sentence:
            time.sleep(1)
            continue

        intent = intent_recognize(sentence)
        intent_name = intent["intent"]["name"]
        intent_slot = intent["entities"]
        action = getattr(actions, f"Action{intent_name.capitalize()}")(
            intent_name, intent_slot
        )
        reply(action)


if __name__ == "__main__":
    main()
