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
    st.write('SECTIONS IN THIS RESUME')
    sections = sectionExtractor.get_section_data(parsed_pdf['content'])
    for key in sections:
        expander = st.expander(key, expanded=False)
        with expander:
            st.write(sections[key])

    if 'WorkExperience' in sections:
        workExp = workExpExtractor.extractWorkExp(sections['WorkExperience'])
        st.write('WORK EXPERIENCE')
        st.write(workExp)

    if 'SummaryText' in sections:
        st.write('PERSONAL INFO:')
        c1, c2 = st.columns((1, 1))
        name, email, phone, address = workExpExtractor.getPersonalInfo(sections['SummaryText'])
        with c1:
            st.caption('Complete Name')
            st.markdown(f'`{name}`')
            st.caption('Phone Number:')
            st.markdown(f'`{phone}`')
        with c2:
            st.caption('Email:')
            st.markdown(f'`{email}`')
            st.caption('Address:')
            if len(address) > 0:
                st.markdown(f'`{address[0]}`')
            else:
                st.markdown(f'`No postal  address found`')




