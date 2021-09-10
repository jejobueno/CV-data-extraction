# CV Data Extraction
The aim of the project is to extract and cluster information from a free-format resume which later will be used to match similar Cvs. <br>
**To see the dataset: [Kaggle](https://github.com/arefinnomi/curriculum_vitae_data)**

---------------
### Project Guidelines
- Repository : `CV-data-extraction`
- Duration : `10 days`
- Deadline : `10.09.2021`
- Information to extract:
  -     Personal information: name,surname,email address, postal address, phone number
  -     Education: year, institution name, study name
  -     Previous Job Experience: year, title, organization name
  -     Skills

### Prerequisites
- Python3

### Tools & Libraries

- [SpaCy NLP processing library](https://spacy.io/)
- [Flair NLP library](https://github.com/flairNLP/flair)
- [Apache Tika - Text extractor](https://tika.apache.org/)
- [Pandas - Dataframe, CSV reader](https://pandas.pydata.org/)


### Installation
```
git clone https://github.com/jejobueno/CV-data-extraction
cd CV-data-extraction
pip install -r requirements.txt
```

### Usage
`python main.py`

### Contributors
- [Jesus Bueno](https://github.com/jejobueno)
- [Ceren Morey](https://github.com/c-morey)


