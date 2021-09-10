from tika import parser
from extractSections import SectionExtractor

def getInfoSection(pdf_file):
    parsed_pdf = parser.from_file(pdf_file)
    data_content = parsed_pdf['content']
    sections = SectionExtractor()
    sections = sections.get_section_data(data_content)
    return sections.get("SummaryText")

def getToolsSection(pdf_file):
    parsed_pdf = parser.from_file(pdf_file)
    data_content = parsed_pdf['content']
    sections = SectionExtractor()
    sections = sections.get_section_data(data_content)
    return sections.get("ToolsAndTechnologies")


