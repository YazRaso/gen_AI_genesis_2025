import streamlit as st
from transformers import MT5ForConditionalGeneration, MT5Tokenizer
import torch

"""
This is it! The hot stuff - Yaz
"""

model_path = "./mt5_finetuned"
loaded_model = MT5ForConditionalGeneration.from_pretrained(model_path)
loaded_tokenizer = MT5Tokenizer.from_pretrained(model_path)
loaded_model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
loaded_model.to(device)
try:
    print("Model is ", loaded_model)
except Exception as e:
    raise ValueError(f"Oops, that was not supposed to happen! {e}")

st.write()
language_options = ("Wixarika", "Rarámuri", "Otomí")
st.selectbox("Select Language", language_options)
intro = "Hola 👋 bienvenido a rAIces ☺️"

# TODO: make translate function
st.write(translate(lang=language_options, msg=intro))