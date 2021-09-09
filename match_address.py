from tika import parser
from extractSections import get_section_data
from flair.data import Sentence
from flair.models import SequenceTagger
import re
import spacy


parsed_pdf = parser.from_file("./curriculum_vitae_data/pdf/53.pdf")
content = parsed_pdf['content']
sections = get_section_data(content)


for key in sections.keys():
    if key == "SummaryText":
        address_regex = re.finditer("Address.:?(.*)", sections.get("SummaryText").replace(" ",""), re.IGNORECASE)
        if address_regex:
            for match in address_regex:
                if "@" not in match.group(1):
                    print(match.group(1))

    elif key == "ToolsAndTechnologies":
        address_regex = re.search("Address.:?(.*)", sections.get("ToolsAndTechnologies"), re.IGNORECASE)
        if address_regex:
            if "@" not in address_regex.group():
                print(address_regex.group(1))


# FLAIR
tagger = SequenceTagger.load("ner-large")
sentence = Sentence(sections.get("SummaryText"))
tagger.predict(sentence)

#print(sentence)
print('The following addresses are found:')
for entity in sentence.get_spans('ner'):
    words = [entity]
    for i in words:
        if i.labels[0].value == "LOC":
            print(i.text)

# SPACY to find LOC entity
nlp = spacy.load("en_core_web_lg")
doc = nlp(sections.get("SummaryText"))
for token in doc.ents:
    if token.label_ == 'LOC':
        print(token)


