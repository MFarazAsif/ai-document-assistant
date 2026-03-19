from src.document import Document
from src.rag import RAGPipeline

# load and split document
doc = Document("C:/Users/Faraz/ai_document_assistant/data/sample.pdf")
doc.load()
doc.split()
doc.summary()

# create RAG pipeline
rag = RAGPipeline()

# store chunks as embeddings
rag.store_chunks(doc.chunks)

# ask a real question about the document
question = "What is the purpose of this report?"
answer = rag.ask(question)

print(f"\nQuestion: {question}")
print(f"Answer  : {answer}")