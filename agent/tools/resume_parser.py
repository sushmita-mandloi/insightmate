import fitz
import os
from langchain.tools import Tool
from langchain_groq import ChatGroq

def get_api_key():
    try:
        import streamlit as st
        return st.secrets["GROQ_API_KEY"]
    except:
        return os.getenv("GROQ_API_KEY")

_resume_text = None
_resume_data = None

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"PDF Error: {str(e)}"

def parse_resume(pdf_path: str) -> str:
    global _resume_text, _resume_data
    raw_text = extract_text_from_pdf(pdf_path)
    if "PDF Error" in raw_text:
        return raw_text
    _resume_text = raw_text
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=get_api_key()
    )
    prompt = f"""Analyze this resume and extract:
1. Name
2. Email & Phone
3. Technical Skills
4. Education
5. Experience
6. Projects
7. Certifications

Resume:
{raw_text[:3000]}

Give clear structured response."""
    response = llm.invoke(prompt)
    _resume_data = response.content
    return _resume_data

def get_resume_text():
    return _resume_text

def get_resume_data():
    return _resume_data

resume_parser_tool = Tool(
    name="Resume_Parser",
    description="Parse PDF resume. Input should be the file path only.",
    func=parse_resume
)