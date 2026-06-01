
import streamlit as st
import pandas as pd
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')

faq = pd.read_csv("faq_data.csv")

def preprocess(text):

    text = text.lower()

    tokens = word_tokenize(text)

    stop_words = set(stopwords.words('english'))

    tokens = [
        word for word in tokens
        if word.isalnum()
        and word not in stop_words
    ]

    return " ".join(tokens)

faq["processed"] = faq["Question"].apply(preprocess)

vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform(faq["processed"])

st.title("📑 FAQ Chatbot")

user_question = st.text_input("Ask a Question")

if st.button("GET ANSWER"):
    query = preprocess(user_question)
    query_vector = vectorizer.transform([query])
    similarity = cosine_similarity(query_vector,vectors)
    best_match = similarity.argmax()
    score = similarity.max()
    if score > 0.2:
        answer = faq.iloc[best_match]["Answer"]
        st.success(answer)
        st.write(f"Confidence Score:{score:.2f}")
    else:
        st.warning("Sorry,I don't know the answer.")
