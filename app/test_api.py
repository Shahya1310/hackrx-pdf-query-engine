import requests

def evaluate_query(question, chunks):
    context = "\n\n".join(doc.page_content for doc in chunks)
    prompt = f"""
Context:
{context}

Question:
{question}

Answer step-by-step with reasoning, then conclude with Yes/No and conditions if any.
""".strip()

    # Using a lightweight, no-auth Hugging Face model
    api_url = "https://api-inference.huggingface.co/models/bigscience/bloomz-560m"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200
        }
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            result = response.json()
            if isinstance(result, list) and 'generated_text' in result[0]:
                return result[0]['generated_text']
            else:
                return "Unexpected response format."
        except Exception as e:
            return f"Error parsing model output: {e}"
    else:
        return f"Model error: {response.status_code} - {response.text}"
