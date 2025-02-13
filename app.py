import streamlit as st
import requests
import time

# Initialize session state for conversation and API key
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

# Function to call DeepSeek API
def call_deepseek_api(messages, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'messages': messages,
        'model': 'DeepSeek-R1'
    }
    response = requests.post('https://api.deepseek.com/v1/chat/completions', headers=headers, json=data)
    return response

# Function to handle input focus
def set_user_input_focus():
    st.session_state.user_input_focus = True

# Streamlit UI
st.title("Chat with DeepSeek-R1")

# Prompt for API key if not set
if st.session_state.api_key is None:
    api_key = st.text_input("Enter your API Key to start chatting", type="password", key="api_key_input")
    if st.button("Submit API Key"):
        if api_key:
            st.session_state.api_key = api_key
else:
    user_input = st.text_input("You: ", key="user_input_main", on_change=set_user_input_focus)
    if st.button("Send") or st.session_state.get('user_input_focus', False):
        if user_input:
            # Append user input to conversation
            st.session_state.conversation.append({"role": "user", "content": user_input})
            st.session_state.user_input_focus = False
            
            # Call the API with the full conversation history
            with st.spinner("Thinking..."):
                response = call_deepseek_api(st.session_state.conversation, st.session_state.api_key)
                
                # 检查响应状态码
                if response.status_code == 200:
                    try:
                        json_response = response.json()
                        # 解析API响应，获取AI的回复内容
                        ai_message = json_response['choices'][0]['message']['content']
                    except (KeyError, IndexError, ValueError) as e:
                        ai_message = f"抱歉，无法解析AI的回复。错误: {str(e)}"
                        st.error(f"API响应解析错误: {str(e)}")
                else:
                    # 显示错误状态码和响应内容
                    ai_message = f"抱歉，API请求失败。状态码: {response.status_code}"
                    try:
                        error_content = response.json()
                        st.error(f"API错误信息: {error_content}")
                    except ValueError:
                        st.error(f"API未返回JSON格式的错误信息。响应内容: {response.text}")
                
            # Append AI's reply to conversation
            st.session_state.conversation.append({"role": "ai", "content": ai_message})
    
    # Display conversation
    st.markdown("### Conversation")
    for message in st.session_state.conversation:
        if message['role'] == 'user':
            st.write(f"**You:** {message['content']}")
        else:
            st.write(f"**AI:** {message['content']}")

    # Clear conversation button
    if st.button("Clear Conversation"):
        st.session_state.conversation = []
    
    # 移除多余的 text_input，避免重复键错误
    # 如果需要实现自动聚焦，可以考虑使用自定义组件或其他方法 
