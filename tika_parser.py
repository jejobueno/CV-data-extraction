from tika import parser
import re
from extractSections import get_section_data

def get_section(pdf_file):
    parsed_pdf = parser.from_file(pdf_file)
    data_content = parsed_pdf['content']
    data_content = re.sub(" +", " ", data_content)
    section = get_section_data(data_content)
    return section.get("SummaryText")
    #return section[0][1]


info_section = get_section("./curriculum_vitae_data/pdf/31.pdf")



