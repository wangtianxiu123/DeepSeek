import streamlit as st
import requests
import time

# Initialize session state for conversation and API key
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

# Function to call DeepSeek API
def call_deepseek_api(prompt, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': prompt,
        'model': 'DeepSeek-R1'
    }
    response = requests.post('https://api.deepseek.com/v1/chat', headers=headers, json=data)
    return response.json()

# Function to handle input focus
def set_user_input_focus():
    st.session_state.user_input_focus = True

# Streamlit UI
st.title("Chat with DeepSeek-R1")

# Prompt for API key if not set
if st.session_state.api_key is None:
    api_key = st.text_input("Enter your API Key to start chatting", type="password")
    if st.button("Submit API Key"):
        if api_key:
            st.session_state.api_key = api_key
else:
    user_input = st.text_input("You: ", key="user_input", on_change=set_user_input_focus)
    if st.button("Send") or st.session_state.get('user_input_focus', False):
        if user_input:
            # Append user input to conversation
            st.session_state.conversation.append({"role": "user", "content": user_input})
            st.session_state.user_input_focus = False
            
            # Call the API
            with st.spinner("Thinking..."):
                response = call_deepseek_api(user_input, st.session_state.api_key)
                thought_process = response.get('thought_process', '...')
                reply = response.get('reply', '...')
            
            # Simulate thought process
            st.session_state.conversation.append({"role": "ai", "content": f"Thinking: {thought_process}"})
            time.sleep(2)  # Simulate delay for thought process
            st.session_state.conversation.append({"role": "ai", "content": reply})

    # Display conversation
    st.markdown("### Conversation")
    for message in st.session_state.conversation:
        if message['role'] == 'user':
            st.write(f"You: {message['content']}")
        else:
            st.write(f"AI: {message['content']}")

    # Clear conversation button
    if st.button("Clear Conversation"):
        st.session_state.conversation = []

    # Auto-focus on input box
    st.text_input("You: ", key="user_input", on_change=set_user_input_focus) 
