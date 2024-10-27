import streamlit as st
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Load FAQs data
def load_faqs():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'FAQs_-_01042022.json')
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        faqs = []
        for section in data['iOSfaqs']['sections']:
            section_name = section['sec_name']
            for qa in section['sec_data']:
                faqs.append({
                    'section': section_name,
                    'question': qa['q'],
                    'answer': qa['a']
                })
        return faqs
    except FileNotFoundError:
        st.error("FAQ file not found. Please check the file path.")
        return []
    except json.JSONDecodeError:
        st.error("Error reading FAQ file. Please check the file format.")
        return []

def create_context_from_faqs(faqs):
    """Create a context string from FAQs for the system message"""
    context = "You are an NJ Transit support assistant. Here are the official FAQs you should base your answers on:\n\n"
    for faq in faqs:
        context += f"Section: {faq['section']}\n"
        context += f"Q: {faq['question']}\n"
        context += f"A: {faq['answer']}\n\n"
    context += "\nPlease use this information to answer questions. If a question isn't covered in the FAQs, you can provide general help but mention that the information is not from the official FAQs."
    return context

def get_chatbot_response(prompt, conversation_history, faqs_context):
    """Get response from GPT model with FAQs context"""
    try:
        messages = [
            {"role": "system", "content": faqs_context}
        ]
        
        # Limit conversation history to last 5 messages
        recent_history = conversation_history[-5:] if len(conversation_history) > 5 else conversation_history
        
        # Add conversation history
        for msg in recent_history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Add user's new prompt
        messages.append({"role": "user", "content": prompt})
        
        # Updated API call format
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=0.7,
            top_p=1.0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"I apologize, but I'm having trouble responding right now. Please try again later. Error: {str(e)}"

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []

if "faqs" not in st.session_state:
    st.session_state.faqs = load_faqs()
    if st.session_state.faqs:
        st.session_state.faqs_context = create_context_from_faqs(st.session_state.faqs)
    else:
        st.session_state.faqs_context = "You are an NJ Transit support assistant. Please provide general help."

# Chat interface styling
st.markdown("""
<style>
.chat-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 350px;
    max-height: 500px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    z-index: 1000;
}

.chat-header {
    background: #1E90FF;
    color: white;
    padding: 10px;
    border-radius: 10px 10px 0 0;
    font-weight: bold;
}

.chat-messages {
    padding: 10px;
    max-height: 300px;
    overflow-y: auto;
}

.timestamp {
    font-size: 0.7em;
    color: #888;
    margin-top: 2px;
}

.source-info {
    font-size: 0.8em;
    color: #666;
    font-style: italic;
    margin-top: 5px;
}

/* Custom scrollbar */
.chat-messages::-webkit-scrollbar {
    width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.chat-messages::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
}
</style>
""", unsafe_allow_html=True)

# Chat container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Chat header
    st.markdown('<div class="chat-header">💬 NJ Transit Support</div>', unsafe_allow_html=True)
    
    # Messages area
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        try:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "timestamp" in message:
                    st.markdown(f'<div class="timestamp">{message["timestamp"]}</div>', 
                              unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error displaying message: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask about NJ Transit...", key="chat_input"):
        current_time = datetime.now().strftime("%I:%M %p")
        
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": current_time
        })
        
        # Get chatbot response
        response = get_chatbot_response(
            prompt, 
            st.session_state.messages, 
            st.session_state.faqs_context
        )
        
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": current_time
        })
        
        # Rerun to update chat
        st.rerun()

# Clear chat button
if st.button("Clear Chat", key="clear_chat"):
    st.session_state.messages = []
    st.rerun()