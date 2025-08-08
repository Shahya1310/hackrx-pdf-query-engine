from transformers import pipeline

# Load model once at startup
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def evaluate_query(question: str, relevant_chunks: list) -> str:
    """
    Takes a question + relevant document text chunks
    Returns best answer from Hugging Face model
    """
    context = "\n".join(relevant_chunks)
    if not context.strip():
        return "No relevant information found in the document."

    try:
        result = qa_pipeline(question=question, context=context)
        return result.get("answer", "No answer found.")
    except Exception:
        return "Error while generating answer."
