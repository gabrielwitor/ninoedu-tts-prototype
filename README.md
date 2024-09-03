# Abacada tts

Abacada tts é uma aplicação web escrita em Python com Flask. O objetivo é gerar audios sintetizados automaticamente para o projeto NINOEDU da Universidade Estadual do Norte do Paraná.

Há duas funções: **Gerar ZIP** e **Sintetizar áudio**

- **Gerar ZIP:** Gera um arquivo zip de *assets* para os jogos Godot do NINOEDU. No arquivo ZIP há as imagens inseridas pelo usuário e os áudios gerados automaticamente para as imagens, além de um arquivo json com os caminhos das imagens e de seus respectivos áudios. 

- **Sintetizar áudio:** Um simples sintetizador de áudio.

# Como usar o abacada TTS

Primeiro, instale Python em seu computador.

Clone o repositório

```bash
git clone https://github.com/gabrielwitor/ninoedu-tts-prototype
```

Navegue até a pasta do projeto

```bash
cd ninoedu-tts-prototype
```
Crie um ambiente virtual python e ative-o

```bash
python -m venv venv
source .venv/bin/activate
```
Instale as bibliotecas no ambiente virtual

```bash
pip install -r requirements.txt
```

Rode a aplicação e voilà! (Acesse a aplicação web na porta 5000 através do seu navegador)

```bash
python -u app.py
```