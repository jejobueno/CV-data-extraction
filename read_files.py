import docx2txt
import os
import spacy
from spacy.matcher import Matcher
from collections import Counter
from spacy import displacy

from flair.models import SequenceTagger
from flair.data import Sentence

my_path = "curriculum_vitae_data/word"
resume_files = [os.path.join(my_path, f) for f in os.listdir(my_path)
                if os.path.isfile(os.path.join(my_path, f))]

resume = docx2txt.process(resume_files[8])
text_resume = str(resume)

# stanfordnlp.download('en')
# nlp = stanfordnlp.Pipeline()
# doc3 = nlp(text_resume)
# doc3.sentences[5].print_dependencies()


model = SequenceTagger.load('ner-large') #.load('ner')
s = Sentence(text_resume)
model.predict(s)
dict_s = s.to_dict(tag_type='ner')

print(type(dict_s.get('text', 'NO KEY')))
