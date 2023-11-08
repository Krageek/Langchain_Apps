import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx2python import docx2python

load_dotenv()

st.set_page_config(page_title="Question your documents")
st.header("Ask your documents a question")
st.write("This app is designed to let you ask questions based on  PDF and/or Word documents of your choice. It was built on Python using [Streamlit](https://streamlit.io/) for the app, [LangChain's](https://www.langchain.com/) and [OpenAI's](https://openai.com/blog/openai-api) API for the question answering and creating embeddings, [FAISS (Facebook AI Similarity Search)](https://python.langchain.com/docs/integrations/vectorstores/faiss) to be able to search the created embeddings based on the questions being asked, and [docx2python](https://pypi.org/project/docx2python/) + [PyPDF2](https://pypi.org/project/PyPDF2/) for document text-extraction.")
st.write("\n\n")

document = st.file_uploader("Upload your file (PDF or docx)", accept_multiple_files=True, type=["pdf","docx"])

if document:
    total_text = ""
    for file in document:
        file_ext = file.name.split('.')[-1]
        if file_ext == "pdf":
            read_pdf = PdfReader(file)
            for page in read_pdf.pages:
                total_text+=page.extract_text()
        elif file_ext == "docx":
            #doc_file = docx2python(file)
            with docx2python(file) as docx_file:
                #print(docx_content.text)
                #doc_text = docx_file.text
                total_text += docx_file.text

    text_chunks_gen = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap =150,
        length_function=len
    )
    text_chunks = text_chunks_gen.split_text(total_text)

    embeddings = OpenAIEmbeddings()
    embeddings_store = FAISS.from_texts(text_chunks, embeddings)

    show_question = st.text_input("What would you like to know about your documents")
    if show_question:
        text_compared = embeddings_store.similarity_search(show_question)

        def load_openAI():
            model = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
            return model
        
        llm = load_openAI()

        chain = load_qa_chain(llm, chain_type="stuff")
        answer = chain.run(input_documents=text_compared, question = show_question)

        st.write(answer)




