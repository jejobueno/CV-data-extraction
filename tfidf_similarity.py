from tika import parser
import glob
from extractSections import SectionExtractor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


sectioning_extractor = SectionExtractor()
def clean_whitelines(text):
    text_in_lines = [line for line in text.split('\n') if line.strip() != '']
    text = ''
    for line in text_in_lines:
        text += line + '\n'
    return text

file_num = 951

def collect_sections(content : str):
    sections = sectioning_extractor.get_section_data(content)
    right_sections = ''
    if 'Education' in sections:
        right_sections += sections['Education']
    if 'WorkExperience' in sections:
        right_sections += sections['WorkExperience']
    if 'ToolsAndTechnologies' in sections:
        right_sections += sections['ToolsAndTechnologies']
    return right_sections


parsed_pdf = parser.from_file(f"./curriculum_vitae_data/pdf/{file_num}.pdf")
base_document = parsed_pdf['content'].replace("\n", "")

right_sections = collect_sections(base_document)
base_document = clean_whitelines(right_sections)

list_of_documents = []
list_of_paths = []
for filepath in glob.iglob("./curriculum_vitae_data/pdf/*.pdf"):
    print(f"{filepath} started to process.")
    if filepath != f"./curriculum_vitae_data/pdf/{file_num}.pdf":
        parsed_files = parser.from_file(filepath)
        document = parsed_files['content']
        if type(document) == str:
            right_sections = collect_sections(document)
            document = clean_whitelines(right_sections)
            list_of_documents.append(document)
            list_of_paths.append(filepath)
print("All files are loaded.")

def process_tfidf_similarity():
    vectorizer = TfidfVectorizer()

    # To make uniformed vectors, both documents need to be combined first.
    list_of_documents.insert(0, base_document)
    list_of_paths.insert(0, file_num)
    embeddings = vectorizer.fit_transform(list_of_documents)

    cosine_similarities = cosine_similarity(embeddings[0:1], embeddings[1:]).flatten()

    score_indexes = np.argsort(np.array(cosine_similarities))[::-1]

    highest_score = 0
    highest_score_index = 0
    for i, score in enumerate(cosine_similarities):
        if highest_score < score:
            highest_score = score
            highest_score_index = i

    most_similar_document = list_of_documents[highest_score_index]
    most_similar_document_path = list_of_paths[highest_score_index]

    #print("Most similar document by TF-IDF with the score:", most_similar_document, "highes score:",highest_score, "Path number:", most_similar_document_path)
    return score_indexes,cosine_similarities

score_indexes,cosine_similarities = process_tfidf_similarity()
for i in range(10):
    print("************")
    print(list_of_documents[score_indexes[i]])
    print(list_of_paths[score_indexes[i]])