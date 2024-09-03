from flask import Flask, request, render_template, send_file, jsonify
from gtts import gTTS
import os
import json
import zipfile
import shutil

app = Flask(__name__)

# Diretórios para armazenar arquivos gerados
ASSETS_FOLDER = 'assets'
AUDIO_FOLDER = os.path.join(ASSETS_FOLDER, 'audio')
IMAGES_FOLDER = os.path.join(ASSETS_FOLDER, 'images')
JSON_FILE = os.path.join(ASSETS_FOLDER, 'data.json')
ZIP_FILE = 'assets.zip'

# Função para limpar o diretório de assets
def clear_assets():
    if os.path.exists(ASSETS_FOLDER):
        shutil.rmtree(ASSETS_FOLDER)
    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    os.makedirs(IMAGES_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Limpa os diretórios antes de iniciar um novo processo
        clear_assets()

        words_data = []

        # Obtém todos os campos do formulário
        word_blocks = request.form.getlist('word')
        silaba_blocks = request.form.getlist('silaba')
        complemento_silaba_blocks = request.form.getlist('complemento_silaba')
        
        # Adaptação para múltiplos arquivos de imagem por grupo de palavras
        images_blocks = []
        for i in range(len(word_blocks)):
            image_files = request.files.getlist(f'images_{i}')
            images_blocks.append(image_files)

        # Verifica se o número de palavras, sílabas e complementos são iguais
        if not (len(word_blocks) == len(silaba_blocks) == len(complemento_silaba_blocks) == len(images_blocks)):
            return 'Erro: O número de palavras, sílabas e complementos deve ser o mesmo.'

        for i in range(len(word_blocks)):
            word = word_blocks[i]
            silaba = silaba_blocks[i]
            complemento_silaba = complemento_silaba_blocks[i]
            image_files = images_blocks[i]

            # Cria o áudio para a sílaba e para a palavra inteira
            audio_filename = f'{silaba.lower()}.ogg'
            audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
            tts = gTTS(text=silaba, lang='pt', slow=False)
            tts.save(audio_path)

            palavra_audio_filename = f'{word.lower()}.ogg'
            palavra_audio_path = os.path.join(AUDIO_FOLDER, palavra_audio_filename)
            palavra_tts = gTTS(text=word, lang='pt', slow=False)
            palavra_tts.save(palavra_audio_path)

            image_paths = []
            for j, file in enumerate(image_files):
                if file and file.filename:
                    # Cria o nome do arquivo de imagem
                    image_extension = os.path.splitext(file.filename)[1]
                    image_filename = f'{silaba}_{word}_Imagem_{j + 1}{image_extension}'
                    image_path = os.path.join(IMAGES_FOLDER, image_filename)
                    file.save(image_path)
                    image_paths.append({"imagem": f'res://assets/images/{image_filename}'})

            # Monta a estrutura do JSON para cada palavra
            word_data = {
                "palavra": word.upper(),
                "silaba": silaba.upper(),
                "imagens": image_paths,
                "som": f'res://assets/audio/{audio_filename}',
                "palavra_som": f'res://assets/audio/{palavra_audio_filename}',
                "complemento_silaba": complemento_silaba.upper()
            }
            words_data.append(word_data)

        # Salva as informações no arquivo JSON com codificação UTF-8
        with open(JSON_FILE, 'w', encoding='utf-8') as json_file:
            json.dump({"words": words_data}, json_file, indent=4, ensure_ascii=False)

        # Cria o arquivo ZIP
        with zipfile.ZipFile(ZIP_FILE, 'w') as zipf:
            for folder, subfolders, files in os.walk(ASSETS_FOLDER):
                for file in files:
                    file_path = os.path.join(folder, file)
                    zipf.write(file_path, os.path.relpath(file_path, ASSETS_FOLDER))

        # Envia o arquivo ZIP para download
        response = send_file(ZIP_FILE, as_attachment=True, download_name='assets.zip')

        # Remove os arquivos de imagem e áudio após o envio do ZIP
        shutil.rmtree(AUDIO_FOLDER)
        shutil.rmtree(IMAGES_FOLDER)

        return response

    return render_template('upload.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Texto não fornecido.'}), 400

    # Cria o áudio para o texto fornecido
    audio_filename = 'synthesized.ogg'
    audio_path = os.path.join(ASSETS_FOLDER, audio_filename)
    tts = gTTS(text=text, lang='pt', slow=False)
    tts.save(audio_path)

    return send_file(audio_path, as_attachment=True, download_name=audio_filename)

if __name__ == '__main__':
    app.run(debug=True)
