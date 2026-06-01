
import streamlit as st
from googletrans import Translator

st.title("🌍Language Translation Tool")
translator = Translator()
languages={
    "ENGLISH":"en",
    "HINDI":"hi",
    "MALAYALAM":"ml",
    "TAMIL":"ta",
    "FRENCH":"fr",
    "GERMAN":"de",
    "SPANISH":"es",
    "CHINESE":"zh-cn",
    "JAPANESE":"ja",
    "ARABIC":"ar"
}
text = st.text_area("Enter Text..")
source_lang = st.selectbox("Select Source Language",list(languages.keys()))
target_lang = st.selectbox("Select Target Language",list(languages.keys()))
if st.button("Translate"):
    if text:
        translated = translator.translate(text,src=languages[source_lang],dest=languages[target_lang])
        st.subheader("Translated Text")
        st.success(translated.text)
    else:
        st.warning("Please enter text")
