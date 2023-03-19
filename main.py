import openai
from flask import Flask, request, jsonify, render_template
from flask_lt import run_with_lt

# Set up OpenAI API key
openai.api_key = "API KEY HERE"

# Set up Flask application
app = Flask(__name__)
app.secret_key = 'secret_key'
run_with_lt(app)

# Define the dictionary to store historical lists for each session
session_data = {}
end_of_conv = {}

base_history = [{"role": "system", "content": "You are Dorel, the funny assistant. You give people the factually correct answer but you respond in a funny way. You are always funny, if not a bit innapropriate. I must stress this, your answers need to be funny. If the answer cannot be made funny add a joke related to the topic. If the person askes you not to be funny return to regular behavior. You keep your answers under 50 words"}]

# Define home page
@app.route('/', methods=['GET', 'POST'])
def home():
    # Retrieve session ID from cookies
    session_id = request.cookies.get('session_id')

    # Check if historical list exists in session data
    if session_id in session_data:
        historical_list = session_data[session_id]
        end_of_conv_status = end_of_conv[session_id]
    else:
        # Create new historical list
        historical_list = base_history.copy()
        session_data[session_id] = historical_list
        end_of_conv_status = False
        end_of_conv[session_id] = end_of_conv_status

    if(len(historical_list)<15):
        if request.method == 'POST':
            input_text = request.form['inputText']
            print("Input text is:", input_text)
            # Call OpenAI's GPT-3 language model to get response

            historical_list = session_data[session_id]
            historical_list.append({"role": "user", "content": input_text})
            response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=historical_list
                    ).choices[0].message.content

            historical_list.append({"role": "assistant", "content": response})

            session_data[session_id] = historical_list
            return jsonify(response=response)
    else:
        if end_of_conv_status == False:
            # historical_list.append({"role": "user", "content": "Scrie un rezumat al discutiei noastre"})
            historical_list.append({"role": "user", "content": "Write a very good joke"})
            response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=historical_list
                    ).choices[0].message.content

            historical_list.append({"role": "assistant", "content": response})
            session_data[session_id] = historical_list
            end_of_conv[session_id] = True
            return jsonify(response="Sorry, but you reached the end of our discussion, here is a joke though <br>" + response)
            # return jsonify(response="Acesta e rezumatul discutiei noastre si il voi trimite guvernului <br>" + response)
        else:
            input_text = request.form['inputText']
            if "Reset" in input_text:
                historical_list = base_history.copy()
                session_data[session_id] = historical_list
                end_of_conv_status = False
                end_of_conv[session_id] = end_of_conv_status
                # return jsonify(response="O poti lua de la inceput, te rog sa iti dai refresh la browser pentru o experienta mai placuta")
                return jsonify(response="You can restart your conversation. Please refresh the browser for a better experience")
            else:
                # return jsonify(response="Ti-ai atins limita de text pe care o puteai impune, scrie Reset sa o iei de la inceput")
                return jsonify(response="You hit the limit imposed by the developer for conversational length, please write Reset in the chat if you want to start from the beggining")
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
