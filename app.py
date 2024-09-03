from flask import Flask, request, render_template, send_from_directory, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

# Diretórios para armazenar arquivos gerados
UPLOAD_FOLDER = 'static/uploads'
AUDIO_FOLDER = 'static/audio'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('images')
        names = request.form.getlist('image_names')

        if len(files) != len(names):
            return jsonify({'error': 'O número de imagens deve corresponder ao número de nomes.'}), 400

        image_urls = []
        audio_urls = []
        download_urls = []

        for i, file in enumerate(files):
            image = file
            image_name = names[i]
            if image and image_name:
                image_filename = image.filename
                image_path = os.path.join(UPLOAD_FOLDER, image_filename)
                image.save(image_path)
                
                # Criar o áudio com o nome da imagem
                audio_filename = f'{image_name}.mp3'
                audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
                tts = gTTS(text=image_name, lang='pt', slow=False)
                tts.save(audio_path)

                image_urls.append(f'/static/uploads/{image_filename}')
                audio_urls.append(f'/static/audio/{audio_filename}')
                download_urls.append(f'/download/{audio_filename}')

        return jsonify({
            'image_urls': image_urls,
            'audio_urls': audio_urls,
            'download_urls': download_urls
        })

    # Para solicitações GET, renderize o template HTML
    return render_template('upload.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(AUDIO_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(AUDIO_FOLDER):
        os.makedirs(AUDIO_FOLDER)
    app.run(debug=True)
