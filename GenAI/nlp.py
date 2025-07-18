import streamlit as st
import spacy

@st.cache_resource
def load_spacy():
    return spacy.load("en_core_web_sm")

nlp = load_spacy()

def extract_keywords(text):
    doc = nlp(text)
    keywords = set()
    for token in doc:
        if token.pos_ in {"NOUN", "PROPN", "VERB"} and not token.is_stop and token.is_alpha:
            keywords.add(token.lemma_.lower())
    return keywords

def extract_sections(text):
    # Simple heuristics: look for section headers
    sections = {"skills": "", "experience": "", "education": ""}
    lines = text.splitlines()
    current = None
    for line in lines:
        l = line.strip().lower()
        if "skill" in l:
            current = "skills"
        elif "experience" in l or "employment" in l or "work history" in l:
            current = "experience"
        elif "education" in l or "degree" in l:
            current = "education"
        elif current:
            sections[current] += line + "\n"
    return sections 