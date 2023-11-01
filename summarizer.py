import streamlit as st
import os
from gtts import gTTS
import gtts.lang
from io import BytesIO
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import openai
from deep_translator import GoogleTranslator

template = """
    You are a literature expert. You are given some text in its entirety.
    
    You need to summarize the text in a way that anyone with absolutely no idea about the subject or context of the text, can understand the summary you create.
   
    You also need to show some keywords after the summary from the text, that highlight its key concepts or topics.

    Text: {text}

    Remember that your summary has to be in bullet points with keywords after that. Each bullet point of your summary has to be in a new line. It should be formatted like the example below:
    • This is the first sentence of the summary
    • This is the second sentence of the summary
    
    Keywords:

    Based on this, Your summary in bullet points:
"""

prompt = PromptTemplate(
    input_variables=["text"],
    template = template,
)

OPENAI_api_key = os.getenv('OPENAI_API_KEY')


def load_openAI(OPENAI_api_key):
     model = OpenAI(temperature=0, openai_api_key=OPENAI_api_key)
     return model


llm = load_openAI(OPENAI_api_key)

if 'text_summary' not in st.session_state:
    st.session_state.text_summary = None

st.set_page_config(page_title="Text Summarizer")
st.header("Summarizer Web App")

st.write('You often come across an article or a document with a lot of text. It could either be too complicated to read or you simply don\'t have the time to go through all of it. This app could help you with that by summarizing text into easily understandable points. You are also able to translate the summary into a language of your choosing, if you would like to do that. In the event that you prefer that the summary be read out to you, some of the languages have the added functionality of text-to-speech as well.')
st.write("The app was created using [LangChain's](https://www.langchain.com/) and [OpenAI's](https://openai.com/blog/openai-api) API for summarization of the text, while [deep-translator](https://github.com/nidhaloff/deep-translator) was used for the translations and [gTTS (Google Text-to-Speech)](https://github.com/pndurette/gTTS) for the text-to-speech functionality.")
st.write('[Streamlit](https://streamlit.io/) was used to build this Web App.')

st.markdown("## Text Information")

google_languages = GoogleTranslator().get_supported_languages()


user_max_words = 1500
user_max_chars = 7500

def user_text():
    user_input = st.text_area(label = "Text", placeholder="Copy your text here (upto 1500 words or 7500 chars)".format(user_max_words), key="text_input", max_chars=user_max_chars)
    return user_input


tts_lang_lower = {k.lower(): v.lower() for k,v in gtts.lang.tts_langs().items()}
tts_lang_list_lower = list(tts_lang_lower.values())



max_exceed = 0
text_summary = None


text_val = user_text()
if (len(text_val.split()) > 1500):
    st.write("Exceeded word limit of 1500 words")
    max_exceed = 1
else:
    max_exceed = 0

if st.button("Summarize") and (max_exceed == 0):
    if text_val:
        place_file = BytesIO()
        prompt_with_text = prompt.format(text = text_val)
        text_summary = llm(prompt_with_text)
        st.session_state.text_summary = text_summary
        
        
        

if (max_exceed == 0):
    text_summary = st.session_state.text_summary
    st.markdown("## Summary")
    st.write(text_summary)

    place_file = BytesIO()
    
    if text_summary:
        text_speech = gTTS(text_summary, lang='en')
        text_speech.write_to_fp(place_file)
        st.audio(place_file)
    else:
        st.write('Text to speech not available')

    summary_language = st.selectbox('Select language for summary translation:',google_languages)

    if (st.button("Translate")):
        if summary_language != 'english':
            #text_summary = st.session_state.text_summary
            if text_summary:
                translated_summary = GoogleTranslator(source='auto', target=summary_language).translate(text_summary)
                #st.write(text_summary)
                st.markdown("## Translated Summary")
                st.write(translated_summary)
                if (summary_language in tts_lang_list_lower):
                    dict_search = {val: i for i,val in tts_lang_lower.items()}
                    if (dict_search[summary_language]):
                    #speech_lang = dict_search[summary_language]
                        text_speech = gTTS(translated_summary, lang=dict_search[summary_language])
                        text_speech.write_to_fp(place_file)
                        st.audio(place_file)
                    else:
                        st.write('Text-to-Speech not available for translation')

        elif summary_language == 'english':
            st.write('The summary is already in English')
            
