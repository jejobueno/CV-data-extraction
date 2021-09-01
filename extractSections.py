import docx
import re

import nltk
import spacy
from nltk.corpus import stopwords
import docx2txt
import pandas as pd

# load pre-trained model
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_lg')

# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))


def get_section_data(file_name):
    txt = docx2txt.process(file_name)
    doc = nlp(txt)
    matcher = PhraseMatcher(nlp.vocab)

    section_dict = pd.read_csv('./data/section_title.csv')
    section_title = section_dict.columns.to_list()
    section_words = {}

    for section in section_title[1:]:
        section_words[section] = [nlp(text) for text in section_dict[section].dropna(axis=0)]
        matcher.add(section, None, *section_words[section])

    d = []
    matches = matcher(doc)  # id, start, end
    if len(matches) > 0:
        d.append((section_title[0], doc[:matches[0][1] - 1]))
    for index, section in enumerate(matches):
        match_id, start, end = section
        rule_id = nlp.vocab.strings[match_id]

        if index == len(matches) - 1:
            span = doc[end:]
        else:
            span = doc[end: matches[index + 1][1] - 1]

        if str(span.text) != '':
            d.append((rule_id, span.text))
        #print(rule_id, doc[start:end].text)
        # print('{}    -    {}'.format(rule_id, span.string))
        sections = pd.DataFrame(d, columns=['sections', 'text'])
        sections['text'] = sections['text'].apply(lambda x: clean_text(x))


    return sections


def clean_text(text):
    text = str(text).splitlines()
    text = [sent for sent in text if sent != '']
    return text

