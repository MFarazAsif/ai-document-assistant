import sys
sys.path.append('C:/Users/Faraz/ai_document_assistant')

import gradio as gr
import os
from src.document import Document
from src.rag import RAGPipeline
from src.database import create_tables, save_document, save_question, get_history

create_tables()

rag_pipeline = None
current_doc_id = None

def process_document(file):
    global rag_pipeline, current_doc_id

    if file is None:
        return "No file uploaded"

    doc = Document(file.name)
    doc.load()
    doc.split()

    current_doc_id = save_document(
        os.path.basename(file.name),
        doc.total_pages,
        len(doc.chunks)
    )

    rag_pipeline = RAGPipeline()
    rag_pipeline.store_chunks(doc.chunks)

    return f"Ready. {doc.total_pages} pages, {len(doc.chunks)} chunks processed."

def answer_question(question):
    global rag_pipeline, current_doc_id

    if rag_pipeline is None:
        return "Upload a document first"

    if not question:
        return "Type a question first"

    answer = rag_pipeline.ask(question)
    save_question(current_doc_id, question, answer)
    return answer

def get_question_history():
    if current_doc_id is None:
        return "No document uploaded yet"

    history = get_history(current_doc_id)
    if not history:
        return "No questions asked yet"

    result = ""
    for row in history:
        result += f"Q: {row[0]}\n"
        result += f"A: {row[1]}\n"
        result += f"Asked: {row[2]}\n"
        result += "-" * 40 + "\n"
    return result

with gr.Blocks(title="AI Document Assistant") as app:

    gr.Markdown("# AI Document Assistant")
    gr.Markdown("Upload any PDF and ask questions about it")

    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload PDF", file_types=[".pdf"])
            upload_btn = gr.Button("Process Document", variant="primary")
            upload_status = gr.Textbox(label="Status", interactive=False)

        with gr.Column():
            question_input = gr.Textbox(label="Your Question")
            ask_btn = gr.Button("Ask", variant="primary")
            answer_output = gr.Textbox(label="Answer", interactive=False)

    history_btn = gr.Button("Show Question History")
    history_output = gr.Textbox(label="History", interactive=False)

    upload_btn.click(process_document, inputs=file_input, outputs=upload_status)
    ask_btn.click(answer_question, inputs=question_input, outputs=answer_output)
    history_btn.click(get_question_history, outputs=history_output)

app.launch(server_name="0.0.0.0", server_port=7860, share=False)