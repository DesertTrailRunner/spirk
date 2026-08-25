# app.py
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

# Import tool function directly
from mcp_server import save_teen_survey

st.set_page_config(page_title="Tech Workshop Assistant", page_icon="🤖")
st.title("🤖 EY Nottingham-Spirk Touchpoint v2.2")
st.caption("Tell me a bit about yourself to enter the live dashboard!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! Welcome to the event. What's your name, age, and favorite technology?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_prompt := st.chat_input("Type your response here..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
                if not api_key:
                    st.error("🔑 OpenAI API key missing. Please check your configuration.")
                    st.stop()

                # Pass the tool function directly in a list
                llm = ChatOpenAI(
                    model="gpt-4o-mini", 
                    temperature=0.7, 
                    api_key=api_key
                ).bind_tools([save_teen_survey])

                lc_messages = [
                    HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
                    for m in st.session_state.messages
                ]

                response = llm.invoke(lc_messages)

                if response.tool_calls:
                    for tool_call in response.tool_calls:
                        if tool_call["name"] == "save_teen_survey":
                            # Invoke the tool synchronously
                            result = save_teen_survey.invoke(tool_call["args"])
                            
                            if "ERROR:" in result:
                                st.warning("⚠️ Couldn't save your details right now. Please check your details and try again.")
                                final_reply = "I had trouble saving your information to the database, but feel free to keep chatting!"
                            else:
                                st.success("🎉 Your details have been submitted!")
                                final_reply = "Your responses have been safely saved to the live dashboard!"
                else:
                    final_reply = response.content

                st.write(final_reply)
                st.session_state.messages.append({"role": "assistant", "content": final_reply})

            except Exception as err:
                st.error("Oops! Something went wrong on our end. Please try again.")
                print(f"Unhandled Exception: {err}")