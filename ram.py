import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# --- 1. CONNECT TO YOUR CLOUD DATABASE ---
# We check if it is already connected so the app doesn't crash when you refresh
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

# Create a variable called 'db' to talk to your filing cabinet
db = firestore.client()

# --- 2. CONNECT TO GOOGLE AI ---
genai.configure(api_key="AIzaSyCeWSRVdVjF07mZwXaWmcd5VhVGJD3nBcM")
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 3. WEBSITE DESIGN ---
st.title("My AI Coding Tutor 🚀")
st.write("Welcome to the app! I am ready to help you with C++ or any other coding questions.")

# Give the app a memory for continuous chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Show previous messages on the screen
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.write(message.parts[0].text)

# --- 4. THE CHAT BAR ---
user_question = st.chat_input("Ask me a coding question:")

if user_question:
    # 1. Print the user's question
    with st.chat_message("user"):
        st.write(user_question)
    
    # 2. Get the AI's answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(user_question)
                st.write(response.text)
                
                # --- 5. SAVE TO FIREBASE ---
                # This silently creates a folder called "chat_history" and saves the conversation!
                db.collection("chat_history").add({
                    "question": user_question,
                    "answer": response.text
                })
                
            except Exception as e:
                st.error(f"🚨 Secret Error Code: {e}")