import google.generativeai as genai
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 


def set_api():
    # loading variables from .env file
    load_dotenv()  
    return os.getenv("MY_KEY")


def summarise(data):
    key = set_api()
    model = genai.GenerativeModel('gemini-pro')
    genai.configure(api_key=key)
    response = model.generate_content("Summarise the content: "+ data)
    return response.text
