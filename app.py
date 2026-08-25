import streamlit as st
import asyncio
from fastmcp import Client
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

st.set_page_config(page_title="Tech Workshop Assistant", page_icon="🤖", layout="centered")

st.title("🤖 EY Nottingham Spirk Touchpoint v2.0")
st.caption("Tell me a bit about yourself to enter the live dashboard!")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "What's your name, age, and favorite technology?"}
    ]

# Display Messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User Input
if user_prompt := st.chat_input("Type your response here..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)

    # Process with LLM & MCP Tool
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            # Setup FastMCP Client connected to mcp_server.py
            async def process_mcp():
                async with Client("mcp_server.py") as client:
                    tools = await client.get_tools()
                    
                    # Pass tools to OpenAI model
                    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7).bind_tools(tools)
                    
                    # Convert history to LangChain messages
                    lc_messages = []
                    for m in st.session_state.messages:
                        if m["role"] == "user":
                            lc_messages.append(HumanMessage(content=m["content"]))
                        else:
                            lc_messages.append(AIMessage(content=m["content"]))

                    response = await llm.ainvoke(lc_messages)

                    # Check if the model wants to call the MCP tool
                    if response.tool_calls:
                        for tool_call in response.tool_calls:
                            # Call the MCP server function
                            tool_result = await client.call_tool(
                                tool_call["name"], 
                                tool_call["args"]
                            )
                            st.write(f"✅ *Saved touchpoint: {tool_call['args']}*")
                            
                        final_reply = "Got it! Your information has been saved to the leaderboard."
                    else:
                        final_reply = response.content

                    return final_reply

            # Run async execution inside Streamlit
            final_response = asyncio.run(process_mcp())
            st.write(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})