# from chatbot import chatbot
from flask import Flask, render_template, redirect, url_for, request
import json
import random
import requests
from hybrid_intent import pipeline_intent_reg

app = Flask(__name__)
app.static_folder = 'static'
app.template_folder = 'templates'

@app.route("/")
def home():
    return render_template("ui.html")


@app.route("/get")
def get_bot_response():

    userText = request.args.get('msg')
    input_data = {}
    # input_data['message'] = str(userText)
    # input_data['state_tracker_id'] = phone
    # input_data['state_tracker_id'] = str(random.randint(100000, 999999))
    # r = requests.post(url=api_url, json=input_data)
    # chatbot_respose = r.json()
    chatbot_respose = pipeline_intent_reg(userText)
    # print(chatbot_respose)
    mess_response = [item.replace('\n', r'').replace(r'"',r'') for item in chatbot_respose['answers']]
    # mess_response = chatbot_respose['message'].replace('\n', r'').replace(r'"',r'')
    # print('mess_response',mess_response)
    return {"message_list":mess_response}

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
