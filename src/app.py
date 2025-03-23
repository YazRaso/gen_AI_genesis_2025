from zipfile._path import Translator

import streamlit as st
from transformers import MT5ForConditionalGeneration, MT5Tokenizer
import torch

"""
This is it! The hot stuff - Yaz
"""

# Load model
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

# Constant!
LANGUAGE_CODES = {
    "Wixarika": "hch",
    "Rarámuri": "tar",
    "Otomí": "oto",
    "Spanish": "es",
    "English": "en"
}


"""translate (input_lang, output_lang, text)
produces the translated text from input_lang to output_lang
"""


def translate(input_lang, output_lang, text) -> str:

    lang1 = LANGUAGE_CODES.get(input_lang)
    lang2 = LANGUAGE_CODES.get(output_lang)

    if not lang1 or not lang2:
        raise ValueError("Both input and output languages must be defined")
    # NB: It may be deprecated in the current version of mt5 to give input_lang and output_lang
    input_text = f"translate {input_lang} to {output_lang}: {text}"

    inputs = loaded_tokenizer(input_text, return_tensors="pt")

    output_ids = loaded_model.generate(**inputs)

    translated_text = loaded_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return translated_text









st.write()
language_options = ("Wixarika", "Rarámuri", "Otomí")
# TODO: FIX SELECT LANGUAGE PROMPT
st.selectbox("Select Language", language_options)
intro = "Hola 👋 bienvenido a rAIces ☺️"

# TODO: make translate function
st.write(translate(lang=language_options, text=intro))