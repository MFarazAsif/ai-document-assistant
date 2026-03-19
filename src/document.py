# import os = lets us work with files and folders
import os
# PyPDFLoader = opens and reads PDF files
from langchain_community.document_loaders import PyPDFLoader
# load_dotenv = reads your secret key from .env file
from dotenv import load_dotenv

# load the .env file so your API key is available
load_dotenv()

# class = blueprint, Document = name
class Document:

    # __init__ = runs when you create a Document object
    # self = the object itself, path = location of PDF file
    def __init__(self, path):
        self.path = path               # save the file path
        self.pages = []                # empty list — will hold pages later
        self.total_pages = 0           # counter starts at zero

    # def = function, load = name, self = always first
    def load(self):
        loader = PyPDFLoader(self.path)      # open the PDF
        self.pages = loader.load()           # read all pages into list
        self.total_pages = len(self.pages)   # count total pages
        return self.pages                    # return = send pages back

    # summary = print info about this document
    def summary(self):
        print(f"File       : {self.path}")         # f"" = f-string
        print(f"Pages      : {self.total_pages}")  # {} = inject variable
        print(f"First 200 chars : {self.pages[0].page_content[:200]}")  # [:200] = first 200 characters