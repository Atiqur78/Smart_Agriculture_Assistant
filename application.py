import os
from flask import Flask, render_template, request, jsonify,url_for
from werkzeug.utils import secure_filename
import openai
import requests
from gtts import gTTS
import string
import random

## API key(hugging face & OpenAI)
hugging_api = "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"
openai_api = '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'

openai.api_key = openai_api
application = Flask(__name__)
app = application
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'webm'}
os.makedirs('uploads', exist_ok=True)

## using openai to get answer
def get_answer_openai(question):
    completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = [{"role": "system", "content" : "I want you to act like a helpful agriculture chatbot and help farmers with their query"},
                            {"role": "user", "content" : "Give a Brif Of Agriculture Seasons in India"},
                            {"role":"system","content":"In India, the agricultural season consists of three major seasons: the Kharif (monsoon), the Rabi (winter), and the Zaid (summer) seasons. Each season has its own specific crops and farming practices.\n\n1. Kharif Season (Monsoon Season):\nThe Kharif season typically starts in June and lasts until September. This season is characterized by the onset of the monsoon rains, which are crucial for agricultural activities in several parts of the country. Major crops grown during this season include rice, maize, jowar (sorghum), bajra (pearl millet), cotton, groundnut, turmeric, and sugarcane. These crops thrive in the rainy conditions and are often referred to as rain-fed crops.\n\n2. Rabi Season (Winter Season):\nThe Rabi season usually spans from October to March. This season is characterized by cooler temperatures and lesser or no rainfall. Crops grown during the Rabi season are generally sown in October and harvested in March-April. The major Rabi crops include wheat, barley, mustard, peas, gram (chickpeas), linseed, and coriander. These crops rely mostly on irrigation and are well-suited for the drier winter conditions.\n\n3. Zaid Season (Summer Season):\nThe Zaid season occurs between March and June and is a transitional period between Rabi and Kharif seasons. This season is marked by warmer temperatures and relatively less rainfall. The Zaid crops are grown during this time and include vegetables like cucumber, watermelon, muskmelon, bottle gourd, bitter gourd, and leafy greens such as spinach and amaranth. These crops are generally irrigated and have a shorter growing period compared to Kharif and Rabi crops.\n\nThese three agricultural seasons play a significant role in India's agricultural economy and provide stability to food production throughout the year. Farmers adapt their farming practices and crop selection accordingly to make the best use of the prevailing climatic conditions in each season."},
                            {"role":"user","content":question}
                ]
            )
    
    return completion['choices'][0]['message']['content']


## converting text to audio
def text_to_audio(text,filrname):
    tts = gTTS(text)
    os.makedirs('static/audio', exist_ok=True)
    tts.save(f'static/audio/{filrname}.mp3')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if 'audio' in request.files:
        audio = request.files['audio']
        if audio and allowed_file(audio.filename):
            filename = secure_filename(audio.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio.save(filepath)
            transcription = process_audio(filepath)
            return jsonify({'text': transcription})

    text = request.form.get('text')
    if text:
        response = process_text(text)
        return {'text': response['text'],'voice': url_for('static', filename='audio/' + response['voice'])}

    return jsonify({'text': 'Invalid request'})

##  for checking file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

## for processing audio
def process_audio(filepath):
    API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"
    headers = {"Authorization": f"Bearer {hugging_api}"}
    with open(filepath, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    data = response.json()
    return data['text']
    
## for processing text
def process_text(text):
    return_text = get_answer_openai(text)
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=8))
    text_to_audio(return_text,res)
    return {"text":return_text,"voice": f"{res}.mp3"}


if __name__ == '__main__':
    app.run(host="0.0.0.0")

