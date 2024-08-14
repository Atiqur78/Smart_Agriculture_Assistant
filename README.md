# Agriculture Chatbot

This is a simple agriculture chatbot built using Flask, OpenAI, and Hugging Face. The chatbot can answer questions related to agriculture.

## Features

- Uses OpenAI to generate answers to user queries
- Converts text responses to audio using gTTS
- Allows users to upload audio files for transcription
- Processes audio files using the Hugging Face wav2vec2 model

## Requirements

- Python 3.7+
- Flask
- OpenAI
- Hugging Face
- gTTS
- OpenCV

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Set up the API keys for OpenAI and Hugging Face:
   ```python
   hugging_api = "Enter your Hugging Face API key"
   openai_api = "Enter your OpenAI API key"
   ```

## Usage

1. Type a question related to agriculture seasons in India and press enter.
2. The chatbot will generate an answer and convert it to audio.
3. You can also upload an audio file for transcription.

## Contact

For any questions or concerns, please contact at atikurrahman209@gmail.com
