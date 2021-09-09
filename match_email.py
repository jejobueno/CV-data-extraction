import spacy
from spacy.matcher import Matcher
import re


def extract_email(info_section):
    try:
        reg_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', info_section)
        matches = reg_match.group(0)
        return [matches]

    except:
        print("Regex didn't work")
    else:
        nlp = spacy.load('en_core_web_lg')
        doc = nlp(info_section)

        matcher = Matcher(nlp.vocab)
        pattern = [{'LIKE_EMAIL': True}]

        matcher.add('EMAIL', [pattern])

        matches = matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]

            return span.text
