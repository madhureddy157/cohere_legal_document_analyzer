from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
import docx2txt
import PyPDF2
from cohere_utils import (
    argument_mining, entity_relationship_mapping, clause_explanation, summarization,
    legal_chatbot, strategy_suggestions, risk_prediction
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

@app.post("/upload/")
def upload_file(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    if ext == "pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == "docx":
        text = extract_text_from_docx(file_path)
    else:
        return JSONResponse({"error": "Unsupported file type."}, status_code=400)
    return {"filename": file.filename, "text": text}

@app.post("/argument-mining/")
def api_argument_mining(text: str = Form(...)):
    return {"arguments": argument_mining(text)}

@app.post("/entity-relationship/")
def api_entity_relationship(text: str = Form(...)):
    return {"entities": entity_relationship_mapping(text)}

@app.post("/clause-explanation/")
def api_clause_explanation(text: str = Form(...)):
    return {"explanation": clause_explanation(text)}

@app.post("/summarization/")
def api_summarization(text: str = Form(...)):
    return {"summary": summarization(text)}

@app.post("/legal-chatbot/")
def api_legal_chatbot(question: str = Form(...), context: str = Form(None)):
    return {"answer": legal_chatbot(question, context)}

@app.post("/strategy-suggestions/")
def api_strategy_suggestions(text: str = Form(...)):
    return {"strategies": strategy_suggestions(text)}

@app.post("/risk-prediction/")
def api_risk_prediction(text: str = Form(...)):
    return {"risk": risk_prediction(text)}

@app.post("/future-steps/")
def api_future_steps(text: str = Form(...)):
    prompt = f"Suggest future steps in the following legal case.\n\nCase:\n{text}\n\nFuture Steps:"
    from cohere_utils import cohere_generate
    return {"future_steps": cohere_generate(prompt, "future_steps")}
