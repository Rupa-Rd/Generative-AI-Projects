import streamlit as st
from pypdf import PdfReader

def extract_content(file):
    render = PdfReader(file)
    content = ""

    for page in render.pages:
        content += page.extract_text() or ""
    
    return content

st.title("Pdf Reader")
file = st.file_uploader("Upload Your PDF", type=["pdf"])
submit = st.button("Submit")

if file is not None:
    if submit:
        pdf_content = extract_content(file)
        st.write(pdf_content)
        if st.button("Reset"):
            st.rerun()
else:
    st.error("Invalid File")



