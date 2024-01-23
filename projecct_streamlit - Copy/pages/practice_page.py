# app/practice_page.py
import streamlit as st
from apps.utils import get
import spacy
import docx2txt
import fitz  # PyMuPDF
import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import speech_recognition as sr
import pandas as pd
import pyttsx3


UPLOAD_FOLDER = 'upload_files'
marks_csv_path = 'performance/marks.csv'
nlp = spacy.load('en_core_web_sm')

def get_files(UPLOAD_FOLDER):
    # Get the list of files in the uploaded folder
    files = os.listdir(UPLOAD_FOLDER)

    if not files:
        # No files uploaded, handle this condition (e.g., return an empty list or show a message)
        return []

    # Use the top file (assuming the first file in the list) for further processing
    top_file = files[0]
    file_path = os.path.join(UPLOAD_FOLDER, top_file)

    # Extract skills from the resume text
    skills = list(extract_skills_from_resume(file_path))
    return skills

def extract_skills_from_resume(pdf_path):
    # Load spaCy English model
    

    # Read PDF content using PyMuPDF
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()

    # Process text using spaCy
    doc = nlp(text)

    # Define a list of skills (you can customize this list based on your requirements)
    skills_list = ["java", "python", "html","sql","machine learning","DSA","Data Structures and Algorithms"]

    # Extract skills using spaCy and regular expressions
    extracted_skills = []
    for token in doc:
        # Check if the token is a skill (in this example, we're using a simple case-insensitive check)
        if any(re.search(skill, token.text, re.IGNORECASE) for skill in skills_list):
            cleaned_skill = token.text.replace('\uf020', '').strip()  # Remove special character
            extracted_skills.append(cleaned_skill.lower())

    # Remove duplicates
    unique_skills = list(set(extracted_skills))

    return unique_skills



def create_dict_from_csv(skills):
    dict1 = {}
    for skill in skills:
        csv_path = f'csv_files/{skill}.csv'
        if os.path.isfile(csv_path):
            data = pd.read_csv(csv_path)
            rows = data.sample(n=1, replace=False)
            for index, row in rows.iterrows():
                dict1[row.iloc[0]] = row.iloc[1]
    return dict1

def speak_function():
    attempts = 0
    marks = 0
    dict1 = create_dict_from_csv(skills)

    if os.path.isfile(marks_csv_path) and os.path.getsize(marks_csv_path) > 0:
        marks_df = pd.read_csv(marks_csv_path)
        attempts = marks_df.shape[0]
    else:
        marks_df = pd.DataFrame(columns=['attempts', 'marks'])

    # Create an empty container for the text
    result_container = st.empty()

    for key, value in dict1.items():
        engine = pyttsx3.init()
        
        # Update the text within the container
        result_container.markdown(
        f"""
        <div style='background-color: #f0f0f0; padding: 20px; border-radius: 10px; margin: 10px 0; width: 700px; height: 200px;'>
            <p style='font-size: 20px; margin-bottom: 10px;'>Question:</p>
            <p style='font-size: 16px;'>{key}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

        engine.say(key)
        engine.runAndWait()
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Speak now...")
            audio = r.listen(source, timeout=5, phrase_time_limit=10)

        try:
            user_response = r.recognize_google(audio, language='en_in').lower()
        except sr.UnknownValueError:
            user_response = ""
        except sr.RequestError:
            user_response = ""
        print(user_response)

        accuracy = calculate_accuracy(key, user_response)
        print(accuracy)
        if accuracy > 0.5:
            marks += 1
    
    # Append results to the marks.csv file
    new_data = {'attempts': attempts + 1, 'marks': marks}
    marks_df = pd.concat([marks_df, pd.DataFrame([new_data])], ignore_index=True)
    marks_df.to_csv(marks_csv_path, index=False)
    
    result_container.markdown(
        f"""
        <div style='background-color: #f0f0f0; padding: 20px; border-radius: 10px; margin: 10px 0; width: 700px; height: 200px;'>
            <p style='font-size: 30px; margin-bottom: 10px;'>Virtual interview is completed 🤩</p>
            <p style='font-size: 20px;'>Final Marks: {marks}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    return marks

def calculate_accuracy(sentence1, sentence2):
    # Use spaCy for tokenization, lemmatization, and stopword removal
    doc1 = nlp(sentence1)
    doc2 = nlp(sentence2)
    
    # Combine lemmatized tokens excluding stop words
    tokens1 = [token.lemma_ for token in doc1 if not token.is_stop]
    tokens2 = [token.lemma_ for token in doc2 if not token.is_stop]
    
    # Combine tokens into a string
    processed_sentence1 = ' '.join(tokens1)
    processed_sentence2 = ' '.join(tokens2)
    
    # Calculate cosine similarity using CountVectorizer
    vectorizer = CountVectorizer().fit_transform([processed_sentence1, processed_sentence2])
    vectors = vectorizer.toarray()
    similarity = cosine_similarity([vectors[0]], [vectors[1]])[0, 0]

    return similarity



state = get()

# Check if the user is logged in
if not state['is_logged_in']:
    st.error('Please log in to view this page.')
else:
    st.header('Virtual Interview')
    

    skills=get_files(UPLOAD_FOLDER)
    # st.write(skills)

    # Create a button to start the virtual interview
    start_button_clicked = st.button('Start Virtual Interview')

    # Check if the button is clicked
    if start_button_clicked:
        # Hide the button by setting its visibility to False
        st.markdown(
            '''
            
            <style>div.row-widget.stButton > button{visibility:hidden}</style>''',
              unsafe_allow_html=True
            )

        # Call the speak_function
        marks = speak_function()
        



