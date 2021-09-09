import threading
import joblib
import pandas as pd
import streamlit as st
import numpy as np

from utils.extractWorkExp import WorkExpExtractor


@st.cache(allow_output_mutation=True)
def createExtractor():
    return WorkExpExtractor()


st.sidebar.title("RESUME PARSER")
st.sidebar.write('\n')
st.sidebar.header("Upload your CV")

st.sidebar.write('\n')

parameters = dict()

parameters['precision'] = st.sidebar.selectbox('Please select a precision value:',
                                               ('00', '00:00', '00:00:00', '00:00:00.0', '00:00:00.00', '00:00:00.000'))
type_address = st.sidebar.selectbox('Please select type of address:', ('REGO', 'ABBR', 'all'))
parameters['reference_date'] = st.sidebar.date_input('Reference Date', key='reference_date')
parameters['base_value'] = st.sidebar.slider(label='base', min_value=1, max_value=10000, step=1)
parameters['column_options'] = st.sidebar.multiselect('Column selection',
                                                      ['EnterpriseNumber', 'Denomination', 'TypeOfAddress', 'CountryFR',
                                                       'zipcode', 'MunicipalityFR', 'StreetFR', 'NumberHouse'],
                                                      default=['EnterpriseNumber'])
st.sidebar.write("You have selected", len(parameters['column_options']), 'columns')
