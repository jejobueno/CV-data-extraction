from tika import parser
from extractSections import SectionExtractor
import re

#parsed_pdf = parser.from_file("./curriculum_vitae_data/pdf/3.pdf")

def get_section(pdf_file):
    parsed_pdf = parser.from_file(pdf_file)
    data_content = parsed_pdf['content']
    sections = SectionExtractor()
    sections = sections.get_section_data(data_content)
    return sections.get("SummaryText")


info_section = get_section("./curriculum_vitae_data/pdf/3.pdf")


def extract_mobile_number(info):
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1['
                                  r'02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9]['
                                  r'02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9]['
                                  r'02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'),
                       info)

    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number


phone_num = extract_mobile_number(info_section)
print(phone_num)
