def format_response(question, reasoning, chunks):
    return {
        "query": question,
        "answer": "Yes" if "yes" in reasoning.lower() else "No",
        "conditions": [],
        "reasoning": reasoning,
        "source_clauses": [
            {"text_snippet": c.page_content[:200]} for c in chunks
        ]
    }
