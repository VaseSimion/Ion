import openai
from flask import Flask, request, jsonify, render_template

# Set up OpenAI API key
openai.api_key = "KEY HERE"

# Set up Flask application
app = Flask(__name__)

#historical_list = [{"role": "system", "content": "You are a called Ion, the romanian assistent. You speak romanian and you answer anything in short phrases, maximum 150 words"}]
historical_list = [{"role": "system", "content": "You are a called Nikolai, the Danish assistent. You make programming jokes. You speak Danish and you answer anything in short phrases, maximum 150 words"}]

# Define home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        input_text = request.form['inputText']
        print("Input text is:", input_text)
        # Call OpenAI's GPT-3 language model to get response
        historical_list.append({"role": "user", "content": input_text})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=historical_list
        ).choices[0]
        historical_list.append({"role": "assistant", "content": response.message.content})
        print(response.message.content)
        return jsonify(response=response.message.content)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
