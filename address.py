from flair.data import Sentence
from flair.models import SequenceTagger
import re


def getAddress(info: str):
    locations = []
    try:
        address_regex = re.finditer("Address.:?(.*)", info.replace(" ", ""), re.IGNORECASE)
        if address_regex:
            for match in address_regex:
                if "@" not in match.group(1):
                    locations.append(match.group(1))
        return locations
    except :
        print("Address not found.")
    else:
        tagger = SequenceTagger.load("ner-large")
        sentence = Sentence(info)
        tagger.predict(sentence)

        for entity in sentence.get_spans('ner'):
            words = [entity]
            for i in words:
                if i.labels[0].value == "LOC":
                    locations.append(i.text)
        return locations
