import streamlit as st
import requests
import time

# Initialize session state for conversation
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

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

# Streamlit UI
st.title("Chat with DeepSeek-R1")
api_key = st.text_input("Enter your API Key", type="password")

if api_key:
    user_input = st.text_input("You: ", key="user_input", on_change=lambda: st.session_state.user_input_focus = True)
    if st.button("Send") or st.session_state.get('user_input_focus', False):
        if user_input:
            # Append user input to conversation
            st.session_state.conversation.append({"role": "user", "content": user_input})
            st.session_state.user_input_focus = False
            
            # Call the API
            with st.spinner("Thinking..."):
                response = call_deepseek_api(user_input, api_key)
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
    st.text_input("You: ", key="user_input", on_change=lambda: st.session_state.user_input_focus = True) 
