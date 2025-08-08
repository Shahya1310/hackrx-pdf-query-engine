import re

# Define a mock document class with a `page_content` attribute
class MockDoc:
    def __init__(self, text):
        self.page_content = text

# Function to split text into clauses or fallback to sentences
def chunk_clauses(text):
    clause_pattern = r"(Clause\s\d+(\.\d+)*[:\-])"
    split_points = [m.start() for m in re.finditer(clause_pattern, text)]
    clauses = []

    if split_points:
        for i in range(len(split_points)):
            start = split_points[i]
            end = split_points[i+1] if i+1 < len(split_points) else len(text)
            chunk = text[start:end].strip()
            if chunk:
                clauses.append(chunk)
    else:
        # Fallback: split by sentence or newline
        sentences = re.split(r'(?<=[.!?])\s+|\n+', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                clauses.append(sentence)

    return clauses

# Evaluate the question using OpenAI or other language model
def evaluate_query(question, chunks):
    # Join all chunk texts
    context = "\n\n".join(doc.page_content for doc in chunks)
    
    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer step-by-step with reasoning, then conclude with Yes/No and conditions if any.
    """

    # Example: using OpenAI (replace with your actual model logic if needed)
    from openai import OpenAI
    client = OpenAI(api_key="your-api-key-here")  # Replace with valid key

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


# ==== Example Usage ====
if __name__ == "__main__":
    input_text = """
    Clause 1: This is the first clause about AI.
    Clause 2: This clause discusses machine learning and its impact.
    Clause 3.1: This sub-clause explains supervised learning.
    This sentence is not in a clause format.
    """

    question = "What is AI?"
    
    # Step 1: Chunk the clauses
    raw_chunks = chunk_clauses(input_text)

    # Step 2: Wrap them in MockDoc format
    chunks = [MockDoc(c) for c in raw_chunks]

    # Step 3: Evaluate the query
    answer = evaluate_query(question, chunks)
    
    print("Answer:\n", answer)
