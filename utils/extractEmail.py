import spacy
from spacy.matcher import Matcher
import re


def getEmail(info: str):
    try:
        reg_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', info)
        matches = reg_match.group(0)
        return [matches]
    except:
        print("Regex didn't work")
    else:
        nlp = spacy.load('en_core_web_lg')
        doc = nlp(info)

        matcher = Matcher(nlp.vocab)
        pattern = [{'LIKE_EMAIL': True}]

        matcher.add('EMAIL', [pattern])

        matches = matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]

            return span.text
