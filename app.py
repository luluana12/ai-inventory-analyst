import streamlit as st
from agent.inventory_agent import run_agent

st.set_page_config(page_title = "AI Inventory Analyst", layout = "wide")

st.title("AI Inventory Analyst")
st.caption("Ask questions about the inventory health of your cruise ships.")

# Stores chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
user_input = st.chat_input("Ask me about inventory health...")
if user_input:
    st.session_state.chat_history.append({"role" : "user", "content" : user_input})
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing inventory, running queries, thinking..."):
            reply = run_agent(
                user_input,
                [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[:-1]]
            )
            st.write(reply)
        st.session_state.chat_history.append({"role" : "assistant", "content": reply})
         
