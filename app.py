from flask import Flask, render_template, request, send_file
import os
from googletrans import Translator
from gtts import gTTS

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

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

    # 🔥 Temporary text (AI remove kiya for stability)
    text = "Hello this is test video"

    # Translate
    translated = translator.translate(text, dest=lang).text

    # Text to speech
    output_audio = "output.mp3"
    tts = gTTS(translated, lang=lang)
    tts.save(output_audio)

    final_video = os.path.join(OUTPUT_FOLDER, "final.mp4")

    # Merge audio with video
    os.system(f'ffmpeg -i "{input_path}" -i {output_audio} -c:v copy -map 0:v:0 -map 1:a:0 "{final_video}"')

    return send_file(final_video, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
