import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

PERSIST_DIRECTORY = os.path.join(os.getcwd(), "data", "chroma_db")

def get_embeddings():
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIEmbeddings(model="text-embedding-3-small")
    elif os.getenv("GOOGLE_API_KEY"):
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    else:
        raise ValueError("No API Key for Embeddings")

class RAGStore:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.vectorstore = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=self.embeddings,
            collection_name="math_knowledge"
        )
        # Memory Store for solved problems
        self.memory_store = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=self.embeddings,
            collection_name="math_memory"
        )
    
    def add_documents(self, docs):
        """
        Docs: List of LangChain Document objects
        """
        self.vectorstore.add_documents(docs)

    def retrieve(self, query, k=3):
        return self.vectorstore.similarity_search(query, k=k)
    
    def add_to_memory(self, problem_text, solution_text, topic):
        from langchain_core.documents import Document
        doc = Document(
            page_content=f"Problem: {problem_text}\nSolution: {solution_text}",
            metadata={"source": "user_memory", "topic": topic}
        )
        self.memory_store.add_documents([doc])
        
    def retrieve_memory(self, query, k=1):
        return self.memory_store.similarity_search(query, k=k)
    
    def as_retriever(self):
        return self.vectorstore.as_retriever()
