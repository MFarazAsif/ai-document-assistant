import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

load_dotenv(dotenv_path=Path("C:/Users/Faraz/ai_document_assistant/.env"))

class RAGPipeline:

    def __init__(self):
        # free embeddings — runs locally, no API cost
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        self.vectorstore = None
        # Groq LLM — free and fast
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

    def store_chunks(self, chunks):
        # convert chunks to embeddings and store in ChromaDB
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory="data/chroma"
        )
        print(f"Stored {len(chunks)} chunks in vector database")

    def search(self, query, k=3):
        # find top k most relevant chunks
        results = self.vectorstore.similarity_search(query, k=k)
        return results

    def ask(self, question):
        # get relevant chunks from vectorstore
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(question)

        # join chunks into one context block
        context = "\n".join([doc.page_content for doc in docs])

        # build prompt with context and question
        prompt = f"""
        Use the context below to answer the question.
        If you don't know, say I don't know.
        Context: {context}
        Question: {question}
        Answer:"""

        # send to Groq and get answer
        response = self.llm.invoke(prompt)
        return response.content  # .content = actual text answer