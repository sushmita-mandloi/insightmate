# agent/tools/resume_parser.py
# Resume Parser Tool — PDF resume se information extract karta hai

import fitz  # PyMuPDF
import os
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Global variable — parsed resume data
_resume_text = None
_resume_data = None

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    PDF file se raw text extract karta hai.
    PyMuPDF (fitz) use karta hai.
    """
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
    """
    Resume PDF ko parse karke structured information extract karta hai.
    GPT-4o use karta hai intelligent extraction ke liye.
    """
    global _resume_text, _resume_data
    
    # Step 1: PDF se text extract karo
    raw_text = extract_text_from_pdf(pdf_path)
    
    if "PDF Error" in raw_text:
        return raw_text
    
    _resume_text = raw_text
    
    # Step 2: GPT-4o se structured data extract karo
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    prompt = f"""
    Yeh resume text hai. Isse analyze karke structured information extract karo.
    
    Resume Text:
    {raw_text[:3000]}
    
    Yeh information extract karo:
    1. Name
    2. Email
    3. Phone
    4. Skills (technical skills ki list)
    5. Education (degree, college, year)
    6. Experience (company, role, duration)
    7. Projects (project names aur technologies)
    8. Certifications
    
    Hindi aur English mix mein friendly format mein do.
    """
    
    response = llm.invoke(prompt)
    _resume_data = response.content
    
    return _resume_data

def get_resume_text():
    """Raw resume text return karo (skill gap analysis ke liye)."""
    return _resume_text

def get_resume_data():
    """Parsed resume data return karo."""
    return _resume_data

# LangChain Tool object banao
resume_parser_tool = Tool(
    name="Resume_Parser",
    description="""
    PDF resume ko parse karke structured information extract karne ke liye use karo.
    PDF file ka path provide karo.
    
    Example:
    "resume parse karo: C:/Users/user/resume.pdf"
    """,
    func=parse_resume
)