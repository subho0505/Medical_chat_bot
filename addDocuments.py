import argparse
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
# For local embedding, use:
from langchain.embeddings import HuggingFaceEmbeddings

def load_and_split_pdfs_from_folder(folder_path):
    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                print(f"Loading {pdf_path}")
                try:
                    loader = PyPDFLoader(pdf_path)
                    pages = loader.load()
                    chunks = splitter.split_documents(pages)
                    all_chunks.extend(chunks)
                    print(f" - {len(chunks)} chunks extracted")
                except Exception as e:
                    print(f" ! Failed to process {pdf_path}: {e}")

    return all_chunks

def embed_chunks(chunks, persist_directory="./db"):
    #embeddings = OpenAIEmbeddings()
    # For local embedding use:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_directory)
    vectordb.persist()
    return vectordb

def main():
    parser = argparse.ArgumentParser(description="Add all PDFs in a folder to vector DB")
    parser.add_argument("folder_path", type=str, help="Path to folder containing PDFs")
    parser.add_argument("--db", type=str, default="./db", help="Directory to store vector DB")
    args = parser.parse_args()

    if not os.path.exists(args.folder_path) or not os.path.isdir(args.folder_path):
        print("Error: folder does not exist or is not a directory.")
        return

    print(f"Scanning folder: {args.folder_path}")
    chunks = load_and_split_pdfs_from_folder(args.folder_path)
    print(f"Total chunks from all PDFs: {len(chunks)}")

    embed_chunks(chunks, persist_directory=args.db)
    print(f"All PDFs successfully added to vector DB at {args.db}")

if __name__ == "__main__":
    main()
