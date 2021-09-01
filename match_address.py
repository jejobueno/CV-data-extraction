import os
import docx2txt
import spacy
from spacy import displacy
from spacy.matcher import Matcher

my_path = "curriculum_vitae_data/word"
resume_files = [os.path.join(my_path, f) for f in os.listdir(my_path)
                if os.path.isfile(os.path.join(my_path, f))]

resume = docx2txt.process(resume_files[3])
text_resume = str(resume)

nlp = spacy.load('en_core_web_lg')
doc = nlp(text_resume)

for token in doc.ents:
    if token.label_ == 'LOC':
        print(token)


