# pip install langchain langchain-openai langchain-chroma langchain-huggingface \
#             langchain-community pypdf sentence-transformers gradio python-dotenv

#from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
#from langchain_ollama import OllamaEmbeddings
from bs4 import BeautifulSoup

def build_index(urls):

    documents = []

    for url in urls:
        docs = WebBaseLoader(url).load()
        documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    embedder = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(
        chunks,
        embedder
    )

    return db


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
#from langchain_ollama import ChatOllama
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

#model = ChatOpenAI( model="llama3", temperature=0)


prompt = ChatPromptTemplate.from_template("""
You are a helpful web page assistant. Answer the question using ONLY the context below.
If the context doesn't contain the answer, say "I couldn't find that in the document."
After your answer, list the page numbers you used as: Sources: page X, page Y.

Context:
{context}

Question: {question}
""")

def ask(db, question):

    chunks = db.similarity_search(question, k=4)

    context = "\n\n".join(
        chunk.page_content
        for chunk in chunks
    )

    chain = prompt | model

    return chain.invoke(
        {
            "context": context,
            "question": question,
        }
    ).content

import gradio as gr

state = {"db": None}                    # ① remember the index across turns

def upload(urls):

    url_list = [
        url.strip()
        for url in urls.splitlines()
        if url.strip()
    ]

    state["db"] = build_index(url_list)

    return f"✅ Indexed {len(url_list)} URLs"

def chat(message, history):
    if state["db"] is None:
        return "Please upload a web link first 📄"
    return ask(state["db"], message)

with gr.Blocks(title="Chat with Websites") as demo:

    gr.Markdown("# 🌐 Chat with Websites (RAG)")

    urls = gr.Textbox(
        lines=5,
        label="Enter URLs (one per line)"
    )

    index_btn = gr.Button("Upload Websites")

    status = gr.Markdown()

    index_btn.click(
        upload,
        inputs=urls,
        outputs=status
    )

    gr.ChatInterface(fn=chat)

demo.launch(share=True)