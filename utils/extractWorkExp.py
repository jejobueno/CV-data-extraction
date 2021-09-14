from difflib import SequenceMatcher

import joblib
from flair.data import Sentence
import pandas as pd
import nltk
import spacy
import re
from spacy.matcher import PhraseMatcher


class WorkExpExtractor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        self.tagger = joblib.load('./models/taggerONTONOTES.pkl')
        self.professions_matcher = self.chargeMatcher('./data/professions.csv', 'professions')
        self.dates = list()
        self.jobs = list()
        self.orgs = list()

    def extractDates(self, workExperience: str):
        sentence = Sentence(workExperience)
        print(sentence)

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

        print(self.jobs, self.dates, self.orgs)

        workExpDf = pd.DataFrame({'job_title': self.jobs,
                                  'period': self.dates,
                                  'company': self.orgs})

        return workExpDf

    def chargeMatcher(self, filepath: str, name: str):
        words_dict = pd.read_csv(filepath, names=[name])

        matcher = PhraseMatcher(self.nlp.vocab)
        matcher.add(name, None, *[self.nlp(text) for text in words_dict[name].dropna(axis=0)])
        return matcher

    def getEmail(self, summaryText: str):
        try:
            reg_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', summaryText)
            matches = reg_match.group(0)
            return [matches]
        except:
            print("Regex didn't work")
        else:
            doc = self.nlp(info)

            matcher = Matcher(nlp.vocab)
            pattern = [{'LIKE_EMAIL': True}]

            matcher.add('EMAIL', [pattern])

            matches = matcher(doc)

            for match_id, start, end in matches:
                span = doc[start:end]

                return span.text

    @staticmethod
    def extract_mobile_number(summaryText: str):
        phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1['
                                      r'02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9]['
                                      r'02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9]['
                                      r'02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'),
                           summaryText)

        if phone:
            number = ''.join(phone[0])
            if len(number) > 10:
                return '+' + number
            else:
                return number

    def getPersonalInfo(self, summaryText: str):
        emails = self.getEmail(summaryText)
        # model = SequenceTagger.load('ner-large')
        s = Sentence(summaryText.lower())
        # model = joblib.load("./model/ner-large-model.pkl")

        self.tagger.predict(s)

        person_names = []
        for entity in s.get_spans('ner'):
            if entity.labels[0].value == "PER":
                person_names.append(entity.text)
            else:
                name_regex = re.search("Name.:?(.*)", summaryText, re.IGNORECASE)
                if name_regex:
                    name = name_regex.group(1).replace(':', '')
                    name = name.strip()
                    person_names.append(name)
        name = certificate_name(person_names, emails[0])
        if name == '':
            if len(person_names) > 0:
                name = person_names[0]
            else:
                name = 'No name found'
        phone = self.extract_mobile_number(summaryText)
        address = self.getAddress(summaryText)
        return name, emails[0], phone, address

    def getAddress(self, summaryText: str):
        locations = []
        try:
            address_regex = re.finditer("Address.:?(.*)", summaryText.replace(" ", ""), re.IGNORECASE)
            if address_regex:
                for match in address_regex:
                    if "@" not in match.group(1):
                        locations.append(match.group(1))
            return locations
        except:
            print("Address not found.")
        else:
            self.tagger.predict(sentence)

            for entity in sentence.get_spans('ner'):
                words = [entity]
                for i in words:
                    if i.labels[0].value == "LOC":
                        locations.append(i.text)
            return locations


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def certificate_name(names, email):
    good_name = ''
    for name in names:
        prob = similar(name, email)
        if prob > similar(good_name, email):
            good_name = name
    return good_name
