from src.document import Document

# create document object
doc = Document("C:/Users/Faraz/ai_document_assistant/data/sample.pdf")

# load the PDF
doc.load()

# split into chunks
doc.split()

# print summary
doc.summary()

# show first 5 chunks in a table
df = doc.chunks_summary()
print(df.head())  # head() = show first 5 rows