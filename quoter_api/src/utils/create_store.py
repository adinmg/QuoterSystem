from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import DataFrameLoader
from langchain_openai import OpenAIEmbeddings
import pandas as pd
from pathlib import Path

def create_or_update_vector_store(file_path: Path):
    # Check if the Excel file exists
    if not file_path.exists():
        print("[INFO] Excel file not found. Vector Store will not be created.")
        return None
    
    try:
        """Create Vector Store from Excel File Path"""
        # Load the Excel file and parse the first sheet
        data = pd.ExcelFile(file_path)
        sheet_names = data.sheet_names
        df = data.parse(sheet_names[0])

        # Load the DataFrame into documents
        loader = DataFrameLoader(data_frame=df, page_content_column=df.columns[0])
        documents = loader.load()

        # Create a FAISS Vector Store from the documents using OpenAI embeddings
        vector_store = FAISS.from_documents(documents=documents, 
                                            embedding=OpenAIEmbeddings())
        
        # Save the Vector Store locally
        FAISS.save_local(vector_store, folder_path="./data/store")
        
        print("[INFO] Vector Store Created.")
        
    except Exception as e:
        print(e)
        vector_store = None
    
    return vector_store

def load_vector_store(folder_path="./data/store"):
    # Check if the Vector Store exists locally
    if Path(folder_path, "index.faiss").exists():
        try:
            # Load the FAISS Vector Store from local storage
            vector_store = FAISS.load_local(folder_path=folder_path,
                                            embeddings=OpenAIEmbeddings(),
                                            allow_dangerous_deserialization=True)
            print("[INFO] Vector Store Loaded.")
            return vector_store
        except Exception as e:
            print("Error Loading Vector Store: ", e)
    else:
        print("Load Excel File to Create Vector Store")
        return None
