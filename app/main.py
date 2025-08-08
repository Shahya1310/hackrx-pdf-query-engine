from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
import fitz  # PyMuPDF
from transformers import pipeline

app = FastAPI()

# Load Hugging Face question answering pipeline (no API key needed)
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

class QARequest(BaseModel):
    documents: str  # PDF URL
    questions: List[str]

@app.post("/hackrx/run")
def ask_questions(req: QARequest):
    try:
        # Download PDF
        response = requests.get(req.documents)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch PDF")

        # Save to temp file
        with open("temp.pdf", "wb") as f:
            f.write(response.content)

        # Extract text
        doc = fitz.open("temp.pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in PDF")

        # Run QA
        answers = []
        for q in req.questions:
            result = qa_pipeline(question=q, context=text)
            answers.append({"question": q, "answer": result['answer']})

        return {"answers": answers}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
