import os
from typing import List
from langchain_community.document_loaders import PyPDFDirectoryLoader, DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Define directory paths
DATA_DIR = "./data_sources"
CHROMA_PERSIST_DIR = "./chroma_db_storage"

# 1. Initialize the embedding model globally
# Using 'all-MiniLM-L6-v2' to keep the CPU/Memory footprint extremely low
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

def get_vector_store() -> Chroma:
    """
    Interface Output Contract: Returns the active, persistent Chroma VectorStore instance.
    If database files don't exist, it processes the raw data and creates it.
    """
    # If the ChromaDB directory already exists and has files, load it immediately to save time
    if os.path.exists(CHROMA_PERSIST_DIR) and len(os.listdir(CHROMA_PERSIST_DIR)) > 0:
        print("🔍 Found existing ChromaDB database. Loading persistent instance...")
        return Chroma(
            persist_directory=CHROMA_PERSIST_DIR, 
            embedding_function=embeddings_model
        )
    
    print("✨ No vector store found. Starting document ingestion pipeline...")
    
    # --- Step A: Load Raw Documents ---
    documents = []
    
    if os.path.exists(DATA_DIR):
        # 1. Process Text Files
        try:
            txt_loader = DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=TextLoader)
            documents.extend(txt_loader.load())
        except Exception as e:
            print(f"⚠️ Warning loading text files: {e}")

        # 2. Process PDF Files Safely One-by-One using PyPDFLoader
        for file in os.listdir(DATA_DIR):
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(DATA_DIR, file)
                try:
                    # PyPDFLoader parses single file paths perfectly and robustly
                    single_pdf_loader = PyPDFLoader(file_path)
                    documents.extend(single_pdf_loader.load())
                except Exception as e:
                    print(f"\n❌ SKIPPING CORRUPTED FILE: {file}")
                    print(f"   Error details: {e}")
                    print("   Please delete this file and redownload it!\n")
    # --- Step B: Chunk Documents Semantic Splitter ---
    # We use RecursiveCharacterTextSplitter as recommended (size 600, overlap 80)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # Maximium characters per chunk
        chunk_overlap=200,     # Shared characters between adjacent chunks
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"✂️ Split documents into {len(chunks)} semantic text chunks.")

    # --- Step C: Generate Embeddings and Save to ChromaDB ---
    print("🧠 Generating embeddings and building local vector database (this may take a minute)...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=CHROMA_PERSIST_DIR
    )
    
    print(f"💾 Vector database successfully built and persisted to '{CHROMA_PERSIST_DIR}'!")
    return vector_store


def retrieve_context(query: str, k: int = 3) -> List[Document]:
    """
    Interface Output Contract: Queries the persistent vector store for the top 'k'
    most semantically relevant document chunks based on the user's input.
    """
    try:
        vector_store = get_vector_store()
        relevant_chunks = vector_store.similarity_search(query, k=k)
        return relevant_chunks
    except Exception as e:
        print(f"❌ Retrieval failed: {e}")
        return []