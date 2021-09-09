import joblib
from flair.data import Sentence
import pandas as pd
import nltk
import spacy
import re
from spacy.matcher import PhraseMatcher


class WorkExpExtractor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.tagger = joblib.load('./models/taggerONTONOTES.pkl')
        self.professions_matcher = self.chargeMatcher('./data/professions.csv', 'professions')
        self.dates = list()
        self.jobs = list()
        self.orgs = list()

    def extractDates(self, workExperience: str):
        sentence = Sentence(workExperience)

        # predict NER tags
        self.tagger.predict(sentence)
        # iterate over entities and print
        dates = []
        for entity in sentence.get_spans('ner'):
            if entity.get_labels()[0].value == 'DATE':
                date = entity.to_dict()
                dates.append(date['text'])

        self.dates = self.dates
        return dates

    def extractJobTitle(self, workExperience: str):
        doc = self.nlp(workExperience)
        matcher = self.professions_matcher
        matches = matcher(doc)
        jobs = []
        for i in range(len(matches)):
            if i < len(matches) - 1:
                if matches[i][1] < matches[i + 1][1] and matches[i][2] >= matches[i + 1][2]:
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

            if not jobs.__contains__(doc[i:j].text):
                jobs.append(doc[start - i + 1:end + j - 1].text)

            self.jobs = jobs

        return jobs

    def extractEnterprise(self, workExperience):
        workex_words = {'date': [self.nlp(text) for text in self.dates], 'job': [self.nlp(text) for text in self.jobs]}

        doc = self.nlp(workExperience)

        matcher = PhraseMatcher(self.nlp.vocab)
        matcher.add('jobs', None, *workex_words['job'])
        matcher.add('date', None, *workex_words['date'])
        matches = matcher(doc)

        orgs = []
        for i in range(len(matches)):
            rule_id, start, end = matches[i]
            if i == len(matches) - 1:
                text = doc[start:].text
            else:
                text = doc[start:matches[i + 1][2]].text
            # make example sentence
            sentence = Sentence(text)

            # predict NER tags
            self.tagger.predict(sentence)
            if doc[start:end].text.__contains__('Freelance'):
                orgs.append('Self Employed')
            for entity in sentence.get_spans('ner'):
                if entity.get_labels()[0].value == 'ORG':
                    org = entity.to_dict()
                    orgs.append(org['text'])
                    break

        return orgs

    def extractWorkExp(self, workExperience):

        workExp = re.sub(r'[()]', '', workExperience)

        self.dates = self.extractDates(workExp)
        self.jobs = self.extractJobTitle(workExp)
        self.orgs = self.extractEnterprise(workExp)

        if len(self.dates) != len(self.jobs):
            self.dates = [None] * len(self.jobs)

        workExpDf = pd.DataFrame({'job_title': self.jobs,
                                  'period': self.dates,
                                  'company': self.orgs})

        return workExpDf

    def chargeMatcher(self, filepath: str, name: str):
        words_dict = pd.read_csv(filepath, names=[name])

        matcher = PhraseMatcher(self.nlp.vocab)
        matcher.add(name, None, *[self.nlp(text) for text in words_dict[name].dropna(axis=0)])
        return matcher
