import docx
import re

import nltk
import spacy
from nltk.corpus import stopwords
import docx2txt
import pandas as pd

# load pre-trained model
from spacy.matcher import PhraseMatcher


class SectionExtractor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        # Grad all general stop words
        self.STOPWORDS = set(stopwords.words('english'))

    def get_section_data(self, txt):
        txt = re.sub(' +', ' ', txt)
        doc = self.nlp(txt)
        matcher = PhraseMatcher(self.nlp.vocab)

        section_dict = pd.read_csv('./data/section_title.csv')
        section_title = section_dict.columns.to_list()
        section_words = {}

        for section in section_title[0:]:
            section_words[section] = [self.nlp(text) for text in section_dict[section].dropna(axis=0)]
            section_words[section] += [self.nlp(text.upper()) for text in section_dict[section].dropna(axis=0)]
            matcher.add(section, None, *section_words[section])

            d = []
            matches = matcher(doc)  # id, start, end
            if len(matches) > 0:
                d.append((section_title[0], clean_whitelines(doc[:matches[0][1]].text)))
            for index, section in enumerate(matches):
                match_id, start, end = section
                rule_id = self.nlp.vocab.strings[match_id]
                if self.nlp(doc[start: end].sent.text)[0:4].text.__contains__(str(doc[start: end])) or doc[
                                                                                                  start - 1: end].text.__contains__(
                    '\n'):
                    if index == len(matches) - 1:
                        span = doc[start:]
                    else:
                        span = doc[start: matches[index + 1][2] - 2]

                    if str(span.text) != '':
                        d.append((rule_id, clean_whitelines(span.text)))
                else:
                    if index == len(matches) - 1:
                        d.append((rule_id, clean_whitelines(doc[start:].text)))
                    else:
                        mutable = list(d.pop(-1))
                        mutable[1] += doc[start - 1:matches[index + 1][2] - 1].text
                        d.append((mutable[0], clean_whitelines(mutable[1])))

        return transform_to_dict(d)



def clean_whitelines(text):
    text_in_lines = [line for line in text.split('\n') if line.strip() != '']
    text = ''
    for line in text_in_lines:
        text += line + '\n'
    return text


def transform_to_dict(d):
    dict_sections = dict()
    for section in d:
        if dict_sections.__contains__(section[0]):
            dict_sections[section[0]] += section[1]
        else:
            dict_sections[section[0]] = section[1]
    return dict_sections
