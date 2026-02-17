import streamlit as st
import requests
import time

# ---------------------------
# App Config
# ---------------------------
st.set_page_config(
    page_title="AI Workflow Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Workflow Assistant")
st.markdown("""
Chat with your AI bot, and see exactly which tool in your workflow is being used in real-time!
""")

# Sidebar: Workflow Status
st.sidebar.header("Workflow Status")
status_placeholder = st.sidebar.empty()
memory_placeholder = st.sidebar.empty()
tool_placeholder = st.sidebar.empty()

# ---------------------------
# Session State
# ---------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "tool_status" not in st.session_state:
    st.session_state.tool_status = {"current_tool": "Idle", "memory": {}, "steps": []}

# ---------------------------
# User Input
# ---------------------------
user_input = st.text_input("Type your message here:")

if st.button("Send") and user_input:
    # Show user message
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    
    # Display current tool as "Processing"
    st.session_state.tool_status["current_tool"] = "Processing..."
    status_placeholder.markdown(f"**Current Tool:** {st.session_state.tool_status['current_tool']}")
    
    # Send request to your n8n webhook
    url = "http://localhost:5678/webhook/557d3f68-3720-499e-8419-1a45c142dbef"
    try:
        response = requests.post(url, json={"message": user_input}, timeout=60)
        if response.status_code == 200:
            bot_response = response.json()[0]["output"]
        else:
            bot_response = f"Error {response.status_code}: Could not get response."
    except Exception as e:
        bot_response = f"Error: {str(e)}"

    # Simulate tool execution visualization
    # (you can enhance this if n8n returns detailed tool info)
    tools_sequence = ["Google Sheets", "Calculator", "Memory", "SerpAPI", "Google Calendar"]
    for tool in tools_sequence:
        st.session_state.tool_status["current_tool"] = tool
        status_placeholder.markdown(f"**Current Tool:** {tool} 🔄")
        memory_placeholder.markdown(f"**Memory Status:** {st.session_state.tool_status['memory']}")
        time.sleep(0.5)  # Simulate execution time

    # Update tool status
    st.session_state.tool_status["current_tool"] = "Idle"
    status_placeholder.markdown(f"**Current Tool:** {st.session_state.tool_status['current_tool']}")
    
    # Add bot response to chat history
    st.session_state.chat_history.append({"role": "bot", "message": bot_response})

# ---------------------------
# Display Chat
# ---------------------------
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['message']}")
    else:
        st.markdown(f"**Bot:** {chat['message']}")
