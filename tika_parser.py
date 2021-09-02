from tika import parser
from extractSections import get_section_data
from match_name_surname import extract_name
from flair.models import SequenceTagger
from flair.data import Sentence

parsed_pdf = parser.from_file("./curriculum_vitae_data/pdf/2.pdf")

data_content = parsed_pdf['content']
# print(data_content)
#name = extract_name(data_content)
#print(name)
section = get_section_data(data_content)
print(section)

# model = SequenceTagger.load('ner-large') #.load('ner')
# s = Sentence(section['text'].iloc[0])
# model.predict(s)
# dict_s = s.to_dict(tag_type='ner')
# print(dict_s)