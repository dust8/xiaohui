"""
NLU 将用户输入的自然语言语句映射为机器可读的结构化语义表达.
一般是由用户意图(user intention)和槽值(slot-value)构成.
可以用序列标注来处理.
"""
import pathlib
import re
from collections import defaultdict

from fuzzywuzzy import fuzz

INTENTS = defaultdict(list)
SLOT_RE = re.compile(r"\[(?P<slot_name>.+?)\]\((?P<slot_value>.+?)\)")


def get_intents():
    intent = None
    root = pathlib.Path(__file__).parent
    path = root.joinpath("data/nlu.md")
    with open(path, encoding="utf8") as fr:
        for line in fr:
            line = line.strip()
            if not line:
                continue

            if line.startswith("## "):
                intent = line[10:]
            elif line.startswith("- "):
                text = SLOT_RE.sub(r"\g<slot_name>", line[2:])
                INTENTS[intent].append(text)


def intent_recognize(sentence):
    result = {
        "intent": {"name": "", "confidence": 0},
        "intent_ranking": [],
        "entities": [],
        "text": sentence,
    }
    max_intent = ""
    max_confidence = 0
    for key, value in INTENTS.items():
        key_max_confidence = 0
        for item in value:
            confidence = fuzz.ratio(sentence, item)
            if confidence > key_max_confidence:
                key_max_confidence = confidence

            if confidence > max_confidence:
                max_intent = key
                max_confidence = confidence

        result["intent_ranking"].append({"confidence": key_max_confidence, "name": key})

    result["intent"]["name"] = max_intent
    result["intent"]["confidence"] = max_confidence

    if max_intent == "open_program":
        result["entities"].append({"entity": "program", "value": sentence[2:]})
    elif max_intent == "search":
        result["entities"].append({"entity": "keyword", "value": sentence[2:]})

    result["intent_ranking"].sort(key=lambda i: i["confidence"], reverse=True)

    return result


get_intents()

if __name__ == "__main__":
    from pprint import pprint

    get_intents()

    # pprint(INTENTS)
    result = intent_recognize("打开git")
    pprint(result)
