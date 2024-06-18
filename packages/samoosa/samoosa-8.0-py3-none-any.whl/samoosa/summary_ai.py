import google.generativeai as genai


def get_api():
    with open("./google-api.txt", "r") as file:
        return file.read()


def summarise(data):
    key = get_api()
    model = genai.GenerativeModel('gemini-pro')
    genai.configure(api_key=key)
    response = model.generate_content("Summarise the content: "+ data)
    return response.text
