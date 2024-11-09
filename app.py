import streamlit as st
from backend import load_and_split_document, initialize_retriever, create_rag_chain, setup_workflow
from langchain_core.messages import HumanMessage, AIMessage
__import__('pysqlite3')
import pysqlite3
import sys

sys.modules["sqlite3"] = pysqlite3

# Load documents and initialize components
documents = load_and_split_document("C:\Users\olivi\OneDrive\Documents\chatbot_fork\22_studenthandbook-22-23_f2.pdf")
retriever = initialize_retriever(documents)
rag_chain = create_rag_chain(retriever)
app = setup_workflow(rag_chain)

# Streamlit User Interface
st.title("Custom Question-Answering Chatbot")
st.write("Ask questions based on the loaded document.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Enter your question here:")

if st.button("Submit"):
    if user_input:
        state = {"input": user_input, "chat_history": st.session_state.chat_history, "context": "", "answer": ""}
        config = {"configurable": {"thread_id": "246"}}
        
        result = app.invoke(state, config=config)
        
        st.session_state.chat_history.append(HumanMessage(user_input))
        st.session_state.chat_history.append(AIMessage(result["answer"]))
        
        st.write("Chatbot:", result["answer"])
    else:
        st.write("Please enter a question.")

