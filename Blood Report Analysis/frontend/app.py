import streamlit as st
from pypdf import PdfReader
from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_URL = os.getenv('FAST_API_URL')

def process_pdf(file):
    render = PdfReader(file)
    pdf_content = ""

    for page in render.pages:
        pdf_content += page.extract_text() or ""

    return pdf_content


def home():
    st.title("Blood Test Report Analysis")
    input = st.file_uploader("Enter your blood test report", type=["pdf"])
    submit = st.button("Start Analysis")

    if input and submit:
        pdf_content = process_pdf(input)
        
        file_uploade_url = API_URL + '/llm'
        payload = {
            'pdf_content': pdf_content
        }
        response = requests.post(file_uploade_url, json=payload)

        if response.status_code == 200:
            st.write(response.json()["analysis"])
        
        analysis_payload = {
        "pdf_content": pdf_content,
        "analysis": response.json()["analysis"]
        }

        upload_result = API_URL + '/result'
        response = requests.post(upload_result, json=analysis_payload)
        


if __name__=="__main__":
    home()