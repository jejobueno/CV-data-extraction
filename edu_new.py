import joblib
from flair.data import Sentence
import pandas as pd
import nltk
import spacy
import re
from spacy.matcher import PhraseMatcher
from extractSections import SectionExtractor
from tika import parser

class EducationExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.tagger = joblib.load("./data/ner-large-model.pkl")
        self.uni_matcher = self.chargeMatcher("./data/world_universities.csv", "universities")
        self.dates = list()
        self.schools = list()
        #self.degrees = list()

    def getDates (self, education_section):
        sentence = Sentence(education_section)
        self.tagger.predict(sentence)
        dates = []
        for entity in sentence.get_spans("ner"):
            if entity.get_labels()[0].value == 'DATE':
                date = entity.to_dict()
                dates.append(date['text'])

        self.dates = dates
        return dates

    def getUniName (self, education_section):
        doc = self.nlp(education_section)
        matcher = self.uni_matcher
        matches = matcher(doc)
        schools = []
        for i in range(len(matches)):
            if i < len(matches) -1:
                if matches[i][1] < matches[i+1][1] and matches[i][2] >= matches[i+1][2]:
                    matches.remove(matches[i])
        for index, section in enumerate(matches):
            match_id, start, end = section
            rule_id = self.nlp.vocab.strings[match_id]
            # print(rule_id, start, end, doc[start:end].text)
            for i in range(5):
                if not re.match(r'^[/a-zA-Z ]+$', doc[start - i:end].text):
                    break
                else:
                    i += 1

            for j in range(5):
                if not re.match(r'^[/a-zA-Z ]+$', doc[start:end + j].text) or doc[start:end + j].text.__contains__(
                        '\n'):
                    break
                else:
                    j += 1

            if not schools.__contains__(doc[i:j].text):
                schools.append(doc[start - i + 1:end + j - 1].text)

            self.schools = schools

        return schools

    def extractEduExp(self, edu_section):

        EduLife = re.sub(r'[()]', '', edu_section)

        self.dates = self.getDates(edu_section)
        self.schools = self.getUniName(edu_section)
        #self.orgs = self.extractEnterprise(workExp)

        if len(self.dates) != len(self.schools):
            self.dates = [None] * len(self.schools)

        EduLifeDf = pd.DataFrame({'school name': self.schools,
                                  'period': self.dates})
                                  #'company': self.orgs})
        return EduLifeDf


    def chargeMatcher(self, filepath: str, name: str):
        words_dict = pd.read_csv(filepath, names=[name])

        matcher = PhraseMatcher(self.nlp.vocab)
        matcher.add(name, None, *[self.nlp(text) for text in words_dict[name].dropna(axis=0)])
        return matcher


parsed_pdf = parser.from_file("./curriculum_vitae_data/pdf/1.pdf")
content = parsed_pdf['content']

sectioning_extractor = SectionExtractor()
sections = sectioning_extractor.get_section_data(content)

eduExtractor = EducationExtractor()
print("starting")
print(eduExtractor.extractEduExp(sections['Education']))
