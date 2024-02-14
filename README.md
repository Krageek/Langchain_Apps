# Langchain_Apps
1. Summarizer App with Langchain and OpenAI

This app is meant to be able to summarize text into a very understandable form while also having the ability to translate the summary into different languages.
There is also the added functionality of using text-to-speech for some of the langugaes for an audio version of the summary.

This app was built in Python using LangChain and OpenAI's API for the summarization. For the translation, deep-translator was used, while gTTS (Google Text-to-Speech) was used for the text-to-speech component.
The app was deployed using Streamlit.



2. Document Question Answering App with Langchain, OpenAI and FAISS

Web Application on Python with Streamlit that can answer user questions based on documents (pdf and docx) uploaded to the application using LangChain and OpenAI. FAISS (Facebook AI Similarity Search) is used to store embeddings and search the embeddings to retrieve content based on the question being asked. docx2python and PyPDF2 are used for file text extraction.
