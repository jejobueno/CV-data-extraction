import joblib
from tika import parser
# opening pdf file
from utils.extractWorkExp import WorkExpExtractor
from utils.extractSections import SectionExtractor

import pandas as pd

pd.set_option('display.max_columns', None)

path = 'data/pdf/1.pdf'
parsed_pdf = parser.from_file('data/pdf/1.pdf')
# saving content of pdf
# you can also bring text only, by parsed_pdf['text']
# parsed_pdf['content'] returns string
data = parsed_pdf['content']

sectionExtractor = SectionExtractor()
sections = sectionExtractor.get_section_data(data)

print('starting extractor')
workExperienceExtractor = WorkExpExtractor()
joblib.dump(workExperienceExtractor, 'workExpExtractor.pkl')

print('starting')
print(workExperienceExtractor.extractWorkExp(sections['WorkExperience']))

workExperienceExtractor


