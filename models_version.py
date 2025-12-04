import google.generativeai as genai
# Configure API KEY
genai.configure(api_key="your_api_key_here")

model = genai.GenerativeModel("gemini-2.5-flash")

# Generate content
response = model.generate_content("Explain how AI works in a few words")

# Print result
print(response.text)
# List all available models
models = genai.list_models()
for model in models:
    print(model.display_name)