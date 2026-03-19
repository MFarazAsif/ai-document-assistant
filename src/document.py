# os = work with files and folders
import os
# load .env file to get API key
from dotenv import load_dotenv
# PyPDFLoader = opens and reads PDF
from langchain_community.document_loaders import PyPDFLoader
# RecursiveCharacterTextSplitter = cuts text into chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter
# pandas = track chunk data in a table
import pandas as pd

load_dotenv()  # read .env file

class Document:

    def __init__(self, path):
        self.path = path       # file location
        self.pages = []        # raw pages
        self.chunks = []       # split chunks
        self.total_pages = 0   # page count

    def load(self):
        loader = PyPDFLoader(self.path)   # open PDF
        self.pages = loader.load()         # read pages
        self.total_pages = len(self.pages) # count pages
        return self.pages                  # send back

    def split(self):
        # chunk_size = max characters per chunk
        # chunk_overlap = how many chars overlap between chunks so context is not lost
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,      # 500 characters per chunk
            chunk_overlap=50     # 50 characters shared between chunks
        )
        # split_documents = cuts all pages into chunks
        self.chunks = splitter.split_documents(self.pages)
        return self.chunks  # send chunks back

    def chunks_summary(self):
        # put chunks into a pandas table for easy viewing
        data = []
        for i, chunk in enumerate(self.chunks):  # enumerate = gives index + value
            data.append({
                "chunk_number": i,                          # which chunk
                "page": chunk.metadata.get("page", 0),     # which page it came from
                "characters": len(chunk.page_content),     # how long
                "preview": chunk.page_content[:80]         # first 80 chars
            })
        df = pd.DataFrame(data)   # DataFrame = table
        return df

    def summary(self):
        print(f"File       : {self.path}")
        print(f"Pages      : {self.total_pages}")
        print(f"Chunks     : {len(self.chunks)}")  # total chunks after splitting