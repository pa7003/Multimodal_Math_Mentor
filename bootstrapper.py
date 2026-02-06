import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rag.store import RAGStore
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter

def bootstrap():
    print("Bootstrapping RAG Knowledge Base...")
    
    kb_path = os.path.join(os.getcwd(), "data", "knowledge_base")
    if not os.path.exists(kb_path):
        print(f"Knowledge base directory not found: {kb_path}")
        return

    # Load all markdown files
    files = [f for f in os.listdir(kb_path) if f.endswith(".md")]
    all_splits = []
    
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    check = set()
    
    for f in files:
        path = os.path.join(kb_path, f)
        with open(path, "r", encoding="utf-8") as file:
            text = file.read()
            
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(text)
        
        # Add source metadata
        for split in md_header_splits:
            split.metadata["source"] = f
            
        all_splits.extend(md_header_splits)
        print(f"Processed {f}: {len(md_header_splits)} chunks")

    if not all_splits:
        print("No documents to add.")
        return

    # Initialize Store and Add
    print(f"Adding {len(all_splits)} chunks to Vector Store...")
    rag = RAGStore()
    rag.add_documents(all_splits)
    print("Done! Vector Store populated.")

if __name__ == "__main__":
    bootstrap()
