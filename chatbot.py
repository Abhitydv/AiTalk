import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer
MODEL_NAME = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Streamlit UI
st.set_page_config(page_title="ChatGPT Clone", layout="centered")
st.title("🤖 ChatGPT Clone - Local")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", key="input")

if user_input:
    st.session_state.chat_history.append(("You", user_input))

    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt").to(device)
    output = model.generate(
        input_ids,
        max_length=250,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        num_return_sequences=1
    )

    bot_response = tokenizer.decode(output[0], skip_special_tokens=True).split(user_input)[-1].strip()
    st.session_state.chat_history.append(("Bot", bot_response))

# Display chat history
for role, msg in st.session_state.chat_history:
    st.markdown(f"**{role}:** {msg}")
