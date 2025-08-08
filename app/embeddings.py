from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

class LocalEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # ✅ Set your model here

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, query):
        return self.model.encode([query])[0].tolist()

local_embedder = LocalEmbeddings()

vectorstore = None

def embed_and_store(clauses):
    global vectorstore
    docs = [Document(page_content=clause) for clause in clauses]
    vectorstore = FAISS.from_documents(docs, embedding=local_embedder)  # ✅ pass the object

def load_vectorstore():
    global vectorstore
    return vectorstore
