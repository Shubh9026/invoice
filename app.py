from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function for gemini and response
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #read the file into bytes
        bytes_data = uploaded_file.get_value()

        image_parts= [
           {
               "mime_type" : uploaded_file.type,
               "data": bytes_data
           }
        ]
        return image_parts
    else:
        raise FileNotFoundError("Not found file")


#intialze our streamlit app

st.header("Multilanguage Invoice Exractore")
input = st.text_input("Input: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the Invoice..", type=["jpg", "jpeg", "png"])
image = " "

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="uploaded image", use_column_width=True)

submit = st.button("Tell me the answer form Invoice")

input_promt="""
You are an expert in understanding the invoice.
we will upload an image of invoice and you have to answer from the invoice.
"""

#if submit is clicked
if submit:
    image_data=input_image_details(uploaded_file)
    response = get_gemini_response(input_promt, image_data, input)
    st.subheader("The response is :")
    st.write(response)