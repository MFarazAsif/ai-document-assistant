from src.document import Document
from src.rag import RAGPipeline
from src.database import create_tables, save_document, save_question, get_history

# create database tables
create_tables()

# load and split document
doc = Document("C:/Users/Faraz/ai_document_assistant/data/sample.pdf")
doc.load()
doc.split()
doc.summary()

# save document to database
doc_id = save_document("sample.pdf", doc.total_pages, len(doc.chunks))
print(f"Document saved with ID: {doc_id}")

# create RAG pipeline
rag = RAGPipeline()
rag.store_chunks(doc.chunks)

# ask questions
questions = [
    "What is the purpose of this report?",
    "What are the main findings?",
]

for question in questions:
    answer = rag.ask(question)
    save_question(doc_id, question, answer)  # save to database
    print(f"\nQ: {question}")
    print(f"A: {answer}")

# show history from database
print("\n--- Question History ---")
history = get_history(doc_id)
for row in history:
    print(f"Q: {row[0]}")
    print(f"A: {row[1][:100]}")  # first 100 chars
    print(f"Asked: {row[2]}")
    print("-" * 30)