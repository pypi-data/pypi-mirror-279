import google.generativeai as genai
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 

# loading variables from .env file
load_dotenv() 


def summarise(data):
    key = os.getenv("MY_KEY")
    model = genai.GenerativeModel('gemini-pro')
    genai.configure(api_key=key)
    response = model.generate_content("Summarise the content: "+ data)
    return response.text
