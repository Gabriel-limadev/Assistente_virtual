"""
Usarei o gtts - Google Text-to-Speech - Para transformar os textos em audios.
"""
import platform
from gtts import gTTS  # Biblioteca principal de transformação de textos em audios
from subprocess import call  # biblioteca para executar o audio no MAC e LINUX
from playsound import playsound  #biblioteca para executar o audio no windows


def cria_audio(texto):
    tts = gTTS(texto, lang='pt-br', slow=False)
    arq = 'audios/bem_vindo.mp3'
    tts.save(arq)

    if platform.system() == 'linux':
        call(['aplay', arq])   # LINUX
    elif platform.system() == 'darwin':
        call(['afplay', arq])  # MAC
    else:
        playsound(arq)


cria_audio(f'Seja bem vindo {platform.node()}')






