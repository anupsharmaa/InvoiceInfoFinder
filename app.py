from genericpath import exists
from tkinter import image_names
from tkinter.messagebox import NO
from turtle import st
from dotenv import load_dotenv

# collect all env var value
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

#configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to call gemini model
def get_gemini(image, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt,image])
    # print(response.text)
    return response.text

    
# stream lit app frontend
st.set_page_config(page_title="InvoiceInfoFinder")
input = st.text_input("Input prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image.." ,type=["jpg","img","png"])
upload_file = None
if uploaded_file is not None:

        file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type}
        st.write(file_details)
        
        tmp=rf"<any/local/path>"
        os.mkdir(tmp,exists=True)
        file_path = os.path.join(tmp, uploaded_file.name)
        # print(file_path)

        with open(file_path,"w") as f: 
          f.write(uploaded_file.getbuffer())   

        st.success("Saved File")

        # print(file_path)
        upload_file = file_path

        image = Image.open(uploaded_file)
        st.image(image,caption="uploade image",use_column_width=True)

submit = st.button("Extract Invoice Details")

# if submit is clicked
if submit:
    # image_data = Image.open('invoice.png')
    image_data = Image.open(upload_file)
    response = get_gemini(image_data,input)

    st.subheader("Response:")
    st.write(response)
