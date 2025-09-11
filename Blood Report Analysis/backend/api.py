from pymongo import MongoClient
from fastapi import FastAPI
from dotenv import load_dotenv
from model import files, analysis
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain 
import os


load_dotenv()
app = FastAPI()
mongodb_client = os.getenv('MONGODB_CLIENT')
API_URL = os.getenv('API_URL')
client = MongoClient(mongodb_client)

db = client["blood_test_analysis"]
file_collections = db["files"]
analysis_collection = db["analysis"]

@app.post('/result')
def store_pdf(analysis_result: analysis):
    result = analysis_collection.insert_one(analysis_result.dict())

    return "Successful!"

@app.post('/llm')
def get_llm_response(file_data: files):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API"))
    prompt = ChatPromptTemplate.from_template("""
    You are a medical AI assistant specialized in blood test interpretation.

    Analyze the following blood test report and present the findings in the following format:

    ### Blood Test Summary Report  
    | Parameter           | Value           | Normal Range        | Interpretation                  |
    |---------------------|------------------|----------------------|----------------------------------|
    | (Fill in each row based on the report. Fill only the elevated interpretation and skip the normal interpretation) |

    ### Summary & Disease Detection  
    Provide a concise summary (under 200 words) highlighting potential health concerns, disease risks, and recommendations. Avoid introductory phrases like "Here is the result" or "Based on the report". Go straight to the analysis.

    Blood Test Report:
    {report_text}
    """)

    chain = LLMChain(llm = llm, prompt=prompt)


    result = chain.run({"report_text": file_data.pdf_content})

   

    return {"analysis": result}



 
