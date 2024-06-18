def set_api():
    api_value = input("Paste the api key: ")
    with open("google-api.txt", "w") as file:
        file.write(api_value)


