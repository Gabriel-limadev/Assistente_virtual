"""
Usarei o gtts - Google Text-to-Speech - Para transformar os textos em audios.
"""
import platform
import speech_recognition as sr
from requests import get
from bs4 import BeautifulSoup

from gtts import gTTS  # Biblioteca principal de transformação de textos em audios
from subprocess import call  # biblioteca para executar o audio no MAC e LINUX
from playsound import playsound  #biblioteca para executar o audio no windows

"""Criação e execução de audios"""


def cria_audio(mensagem, n=0):
    tts = gTTS(mensagem, lang='pt-br', slow=False)
    arq = f'audios/repetir{n}.mp3'
    tts.save(arq)
    with open(arq, 'wb') as mp3:
        tts.write_to_fp(mp3)
    print('ASSISTENTE: ', mensagem)
    executa_audio(arq)


def executa_audio(arq):
    if platform.system() == 'linux':
        call(['aplay', arq])   # LINUX
    elif platform.system() == 'darwin':
        call(['afplay', arq])  # MAC
    else:
        playsound(arq)


""" CONFIGURAÇÕES """
hotword = 'assistente'
with open('jarvis-assistente-327121-994d1596bfa5.json') as credenciais_google:
    credenciais_google = credenciais_google.read()


""" FUNÇÕES """


def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando:")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-br')
                trigger = trigger.lower()
                if hotword in trigger:
                    print('COMANDO: ', trigger)
                    arq = 'audios/audio.mp3'
                    executa_audio(arq)
                    """ executar os comandos """
                    executa_comandos(trigger)
                    break

            except sr.UnknownValueError:
                print("Google Cloud Speech could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger


"""AREA DE CRIAÇÃO DE AUDIOS"""
#cria_audio(f'Seja bem vindo {platform.node()}', 'bem_vindo.mp3')
# cria_audio('só um minuto', )


""" FUNÇÕES """


def executa_comandos(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()
    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem)
        print('COMANDO INVÁLIDO', mensagem)
        executa_audio('audios/mensagem0.mp3')


""" FUNÇÕES DE COMANDO """


def ultimas_noticias():
    site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419')
    noticias = BeautifulSoup(site.text, 'html.parser')
    n = 1
    for item in noticias.findAll('item')[:3]:
        mensagem = item.title.text
        cria_audio(mensagem, n)
        n += 1


def main():
    arq = 'audios/bem_vindo.mp3'
    executa_audio(arq)
    while True:
        monitora_audio()

main()








