import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Get API key safely
google_key = os.getenv("GOOGLE_API_KEY")

if not google_key:
    st.error("GOOGLE_API_KEY not found. Please set it in your .env file")
    st.stop()


# Set up the gemini chat model
llm = ChatGoogleGenerativeAI( model="gemini-pro",google_api_key=google_key)

# Define prompt template
prompt = ChatPromptTemplate.from_template("You are a helpful assistant. Answer this: {question}")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Streamlit UI
st.title("💬 GenAI Chatbot")

#Memory
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    


user_input = st.chat_input("Ask me anything:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        response = chain.invoke({"question": user_input})
        st.session_state.messages.append({"role":"assistant","content":response})
        
    except Exception as e:
        st.error(f"Error: {e}")    

# Chat display

for msg in st.session_state["messages"]:
    st.write(f"**{msg['role'].capitalize()}:** {msg['content']}")