from tika import parser
from extractSections import SectionExtractor
import pandas as pd
import re
import spacy
from spacy.matcher import PhraseMatcher
from nltk.corpus import stopwords
from collections import Counter
from flair.data import Sentence
from flair.models import SequenceTagger

sectioning_extractor = SectionExtractor()
parsed_pdf = parser.from_file("./curriculum_vitae_data/pdf/1.pdf")
content = parsed_pdf['content']
sections = sectioning_extractor.get_section_data(content)

for key in sections.keys():
    if key == 'Education':
        nlp = spacy.load("en_core_web_lg")
        matcher = PhraseMatcher(nlp.vocab)

        csv_file = pd.read_csv("./data/world_universities.csv")
        csv_file.columns = ['Acronym','University','Link']
        uni_names = [nlp(info_section) for info_section in csv_file['University']]

        matcher.add("School_name", None, *uni_names)
        doc = nlp(sections.get("Education"))

        d = []
        matches = matcher(doc)
        for index, section in enumerate(matches):
            match_id, start, end = section
            rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
            span = doc[start: end]  # get the matched slice of the doc
            print(rule_id,doc[start:end].text)
            d.append((rule_id, span.text))
        keywords = "\n".join(f'{i[1]} ({j})' for i,j in Counter(d).items())
        print("keywords:",keywords)

        # make example sentence
        sentence = Sentence(sections.get("Education"))

        tagger = SequenceTagger.load("flair/ner-english-ontonotes-large")
        # predict NER tags
        tagger.predict(sentence)

        # print predicted NER spans
        print('The following NER tags are found:')
        # iterate over entities and print
        dates = []
        school_names = []
        for entity in sentence.get_spans('ner'):
            if entity.get_labels()[0].value == 'DATE':
                date = entity.to_dict()
                dates.append((date['start_pos'], date['end_pos'], date['text']))
                # dates.append(date['text'])
            elif entity.get_labels()[0].value == 'ORG':
                school_name = entity.to_dict()
                # school_names.append((school_name['start_pos'], school_name['end_pos'], school_name['text']))
                school_names.append(school_name['text'])

# schools = []
# #print(len(matches), 'matches=')
# for i in range(len(matches)):
#     if i < len(matches) - 1:
#         if matches[i][1] < matches[i + 1][1] and matches[i][2] >= matches[i + 1][2]:
#             matches.remove(matches[i])
#
# for index, section in enumerate(matches):
#     match_id, start, end = section
#     rule_id = nlp.vocab.strings[match_id]
#     print(rule_id, start, end, doc[start:end].text)
#     for i in range(5):
#         if not re.match(r'^[/a-zA-Z ]+$', doc[start - i:end].text):
#             break
#         else:
#             i += 1
#
#     for j in range(5):
#         if not re.match(r'^[/a-zA-Z ]+$', doc[start:end + j].text):
#             break
#         else:
#             j += 1
#
#     if not schools.__contains__(doc[i:j].text):
#         schools.append(doc[start - i + 1:end + j - 3].text)
#
# print("schools:",schools)





