from utils.extractSections import get_section_data
from tika import parser
# opening pdf file
from utils.extractWorkExp import WorkExpExtractor

import pandas as pd

pd.set_option('display.max_columns', None)

path = 'data/pdf/1.pdf'

parsed_pdf = parser.from_file('data/pdf/1.pdf')
# saving content of pdf
# you can also bring text only, by parsed_pdf['text']
# parsed_pdf['content'] returns string
data = parsed_pdf['content']

sections = get_section_data(data)

print('starting extractor')
workExperienceExtractor = WorkExpExtractor()

print('starting')
print(workExperienceExtractor.extractWorkExp(sections['WorkExperience']))


