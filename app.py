import streamlit as st
import requests
from dotenv import load_dotenv
import os

def call_ollama_api(user_input):
    url = "http://localhost:11434/api/chat"  # Ensure the correct URL
    payload = {
        "model": "llama3",
        "messages": [
            { "role": "user", "content": user_input }
        ],
        "stream": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    
    try:
        response_json = response.json()
        print(response_json)  # Print the raw response for debugging
        return response_json
    except ValueError:
        st.error("Failed to decode JSON response")
        return None

def main():
    load_dotenv()
    st.set_page_config(page_title="Chatbot", page_icon="🤖")
    st.write("<style>body {background-color: #f0f2f6;}</style>", unsafe_allow_html=True)

    st.header("Chatbot 🤖")

    context = st.text_area("Enter the context:, ")
    question = st.text_area("Enter your question:, ")

    if st.button("Submit"):
        full_input = f"Context: {context} Question: {question} Answer only based on the context provided."
        response = call_ollama_api(full_input)
        if response and "message" in response and "content" in response["message"]:
            st.write(response["message"]["content"])
        else:
            st.error("Unexpected response format or no content in response")

if __name__ == "__main__":
    main()
