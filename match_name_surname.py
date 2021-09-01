import spacy
from spacy.matcher import Matcher


def extract_name(info_str):
    names = []
    try:
        nlp = spacy.load("en_core_web_lg")

        matcher = Matcher(nlp.vocab)
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN', "OP": "*"}, {'POS': 'PROPN'}]
        matcher.add('NAME', [pattern])

        doc = nlp(info_str)
        matches = matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            names.append(span.text)
    except:
        return "Spacy POS is not working"
    else:
        person_name = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
        names.extend(person_name)
        return names

    return names


