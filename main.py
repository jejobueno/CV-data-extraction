from utils.extractSections import get_section_data
from tika import parser
# opening pdf file
parsed_pdf = parser.from_file('data/pdf/3.pdf')
# saving content of pdf
# you can also bring text only, by parsed_pdf['text']
# parsed_pdf['content'] returns string
data = parsed_pdf['content']

sections = get_section_data(data)

for section in sections:
    print(section)
    print(sections[section])

