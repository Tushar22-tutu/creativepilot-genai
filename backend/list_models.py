from google import genai

client = genai.Client(api_key="AIzaSyBdT2AlPc1PXlL-ZaLKWXEgtKsiEzdQ9TU")

models = client.models.list()

for model in models:
    print(model.name)