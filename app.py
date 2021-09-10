import threading
import joblib
import pandas as pd
import pdfplumber
import streamlit as st
import numpy as np
from tika import parser
import pdf2image

from utils.extractSections import SectionExtractor
from utils.extractWorkExp import WorkExpExtractor


@st.cache(allow_output_mutation=True)
def createExtractor():
    return WorkExpExtractor(), SectionExtractor()


workExpExtractor, sectionExtractor = createExtractor()

st.sidebar.title("RESUME PARSER")
st.sidebar.write('\n')
uploaded_file = st.sidebar.file_uploader('Please Upload your CV', type="pdf")

if uploaded_file is not None:
    parsed_pdf = parser.from_file(uploaded_file)
    # images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path='utils/poppler-0.68.0/bin')
    # for page in images:
    #    st.sidebar.image(page, use_column_width=True)
    st.write('Sections of the Document')
    sections = sectionExtractor.get_section_data(parsed_pdf['content'])
    st.write(sections)

    if 'WorkExperience' in sections:
        workExp = workExpExtractor.extractWorkExp(sections['WorkExperience'])
        st.write('WORK EXPERIENCE')
        st.write(workExp)

    if 'SummaryText' in sections:
        name, email, phone, address = workExpExtractor.getPersonalInfo(sections['SummaryText'])
        st.write('Name of the Candidate:')
        st.write(name)
        st.write('Email:')
        st.write(email)
        st.write('Phone Number:')
        st.write(phone)
        st.write('Address:')
        st.write(address)


