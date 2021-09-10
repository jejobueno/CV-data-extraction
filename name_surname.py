import re
from Edu_Tools_Section import getInfoSection
from email import getEmail
from flair.models import SequenceTagger
from flair.data import Sentence
import joblib
from difflib import SequenceMatcher



def getName(info: str):
        #model = SequenceTagger.load('ner-large')
        s = Sentence(info.lower())
        # joblib.dump(model,"./data/ner-large-model.pkl")
        model = joblib.load("./data/ner-large-model.pkl")
        model.predict(s)

        person_names = []
        for entity in s.get_spans('ner'):
            if entity.labels[0].value == "PER":
                person_names.append(entity.text)
            else:
                name_regex = re.search("Name.:?(.*)", info, re.IGNORECASE)
                if name_regex:
                    person_names.append(name_regex.group())
        return person_names


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def certificate_name(names, email):
    good_name = ''
    for name in names:
        prob = similar(name, email)
        if prob > similar(good_name, email):
            good_name = name
    return good_name



info_section = getInfoSection("./curriculum_vitae_data/pdf/1.pdf")
emails = getEmail(info_section)
person_names = getName(info_section)

final_name = certificate_name(person_names,emails[0])
print("Final name:",final_name)


