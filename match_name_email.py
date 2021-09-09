from tika import parser
import re
from extractSections import get_section_data
from match_email import extract_email
from flair.models import SequenceTagger
from flair.data import Sentence
import joblib
from difflib import SequenceMatcher

parsed_pdf = parser.from_file("./curriculum_vitae_data/pdf/3249.pdf")
content = parsed_pdf['content']
content = re.sub(" +", " ", content)
sections = get_section_data(content)

for key in sections.keys():
    if key == "SummaryText":
        #model = SequenceTagger.load('ner-large')
        s = Sentence(sections.get("SummaryText").lower())
        #joblib.dump(model,"./data/ner-large-model.pkl")
        model = joblib.load("./data/ner-large-model.pkl")
        model.predict(s)

        person_names = []
        for entity in s.get_spans('ner'):
            if entity.labels[0].value == "PER":
                person_names.append(entity.text)
            else:
                name_regex = re.search("Name.:?(.*)", sections.get("SummaryText"), re.IGNORECASE)
                if name_regex:
                    person_names.append(name_regex.group())
                    #print("final names list:", person_names)

        emails = extract_email(sections.get("SummaryText"))
        print("Emails:",emails)
    else:
        s2 = Sentence(list(iter(sections.values()))[0])
        model = joblib.load("./data/ner-large-model.pkl")
        model.predict(s2)
        names = []
        for entity in s2.get_spans('ner'):
            if entity.labels[0].value == "PER":
                names.append(entity.text)
            else:
                name_regex = re.search("Name.:?(.*)", list(iter(sections.values()))[0], re.IGNORECASE)
                if name_regex:
                    names.append(name_regex.group())
                    #print("Names list:", names)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def certificate_name(names, email):
    good_name = ''
    for name in names:
        prob = similar(name, email)
        if prob > similar(good_name, email):
            good_name = name
    return good_name

final_name = certificate_name(person_names,emails[0])
print("Final name:",final_name)

