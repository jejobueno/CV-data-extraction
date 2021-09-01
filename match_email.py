import spacy
from spacy.matcher import Matcher
import re


def extract_email(info_str):
    try:
        nlp = spacy.load('en_core_web_lg')
        doc = nlp(info_str)

        matcher = Matcher(nlp.vocab)
        pattern = [{'LIKE_EMAIL':True}]

        matcher.add('EMAIL',[pattern])

        matches = matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]

            return span.text
    except:
        print("SpaCy didn't work")
    else:
        reg_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', info_str)
        return reg_match.group(0)

