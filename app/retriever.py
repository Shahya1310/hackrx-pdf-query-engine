from app.embeddings import load_vectorstore

def retrieve_relevant_clauses(query, k=3):
    vectorstore = load_vectorstore()
    return vectorstore.similarity_search(query, k=k)
