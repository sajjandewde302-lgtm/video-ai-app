from flask import Flask, render_template, request, send_file
import os
import whisper
from googletrans import Translator
from gtts import gTTS

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

model = whisper.load_model("tiny")
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']
    lang = request.form['language']

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    audio_path = "audio.mp3"
    output_audio = "output.mp3"
    final_video = os.path.join(OUTPUT_FOLDER, "final.mp4")

    os.system(f'ffmpeg -i "{input_path}" -q:a 0 -map a {audio_path}')

    result = model.transcribe(audio_path)
    text = result["text"]

    translated = translator.translate(text, dest=lang).text

    tts = gTTS(translated, lang=lang)
    tts.save(output_audio)

    os.system(f'ffmpeg -i "{input_path}" -i {output_audio} -c:v copy -map 0:v:0 -map 1:a:0 "{final_video}"')

    return send_file(final_video, as_attachment=True)

import os
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)