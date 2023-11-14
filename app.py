from flask import Flask, render_template, request

# Import the OpenAI library
import openai

app = Flask(__name__)

# Replace with your actual OpenAI API key
api_key = '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'

# Define the translation function
def translate_text(text, source_language, target_language):
    # Define the prompt for translation
    prompt = f"Translate the following text from {source_language} to {target_language}: \"{text}\""

    # Call the OpenAI API for translation
    response = openai.Completion.create(
        engine="text-davinci-002",  # Use GPT-3.5 Turbo engine
        prompt=prompt,
        max_tokens=60,  # Adjust the max tokens as needed
        api_key=api_key
    )

    # Extract the translated text from the API response
    translated_text = response.choices[0].text.strip()

    return translated_text

# Define a function to generate a response based on translated text
def generate_response(translated_text):
    # Make a GPT-3 API call to generate a response based on the translated text
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Generate a response based on the following translated text: \"{translated_text}\"",
        max_tokens=60,  # Adjust the max tokens as needed
        api_key=api_key
    )
    
    # Extract the generated response from the API response
    generated_response = response.choices[0].text.strip()
    
    return generated_response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        source_text = request.form.get("inputText")
        source_language = request.form.get("fromLanguage")
        target_language = request.form.get("toLanguage")

        if source_text and source_language and target_language:
            translated_text = translate_text(source_text, source_language, target_language)
            
            # Generate a response based on the translated text
            generated_response = generate_response(translated_text)
            
            return render_template("index.html", translated_text=translated_text, generated_response=generated_response)

    # Render the initial page or handle invalid input
    return render_template("index.html")

from flask import Flask, render_template, request, jsonify

# ...

@app.route("/translate", methods=["POST"])
def translate():
    if request.method == "POST":
        data = request.get_json()
        source_text = data["inputText"]
        source_language = data["fromLanguage"]
        target_language = data["toLanguage"]

        if source_text and source_language and target_language:
            translated_text = translate_text(source_text, source_language, target_language)
            return jsonify({"translationText": translated_text})

    return jsonify({"error": "Invalid request"})

# ...


@app.route("/process-input", methods=["POST"])
def process_input():
    if request.method == "POST":
        data = request.get_json()
        input_text = data["inputText"]
        from_language = data["fromLanguage"]
        to_language = data["toLanguage"]

        # Translate the input text
        translation_text = translate_text(input_text, from_language, to_language)

        # Generate a response using GPT API based on the translation
        generated_response = generate_response(translation_text)  # Replace with your function call

        # Translate the generated response back to the user's language
        response_translation = translate_text(generated_response, to_language, from_language)

        return jsonify({"translationText": translation_text, "generatedResponse": generated_response, "responseTranslation": response_translation})

    return jsonify({"error": "Invalid request"})

if __name__ == "__main__":
    app.run(debug=True)
