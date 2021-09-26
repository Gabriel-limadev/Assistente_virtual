"""
Usarei o gtts - Google Text-to-Speech - Para transformar os textos em audios.
"""
import platform
import speech_recognition as sr
from requests import get
from bs4 import BeautifulSoup
import webbrowser as browser
import json

from gtts import gTTS  # Biblioteca principal de transformação de textos em audios
from subprocess import call  # biblioteca para executar o audio no MAC e LINUX
from playsound import playsound  #biblioteca para executar o audio no windows

"""Criação e execução de audios"""


def cria_audio(mensagem, nome, n=0):
    tts = gTTS(mensagem, lang='pt-br', slow=False)
    arq = f'audios/{nome}{n}.mp3'
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
                    arq = 'audios/paciencia.mp3'
                    executa_audio(arq)
                    """ executar os comandos """
                    if 'assistente desligar' in trigger:
                        break
                    executa_comandos(trigger)
            except sr.UnknownValueError:
                print("Audio não detectado")
            except sr.RequestError as e:
                print("Comando Invalido".format(e))
    return trigger


""" FUNÇÕES """


def executa_comandos(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()
    elif 'toca beatles' in trigger:
        playlists('beatles')
    elif 'toca queen' in trigger:
        playlists('queen')
    elif 'tempo' in trigger:
        previsao_tempo(tempo=True)
    elif 'temperatura de hoje' in trigger:
        previsao_tempo(minmax=True)
    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem, 'repetir0', '')
        print('COMANDO INVÁLIDO', mensagem)
        executa_audio('audios/pagamento_invalido.mp3')


""" FUNÇÕES DE COMANDO """


def ultimas_noticias():
    site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419')
    noticias = BeautifulSoup(site.text, 'html.parser')
    n = 1
    for item in noticias.findAll('item')[:1]:
        mensagem = item.title.text
        cria_audio(mensagem, 'mensagem0', '')
        n += 1


def playlists(album):
    if album == 'beatles':
        browser.open('https://open.spotify.com/track/6dGnYIeXmHdcikdzNNDMm2?si=989324e902a84cd0')
    elif album == 'queen':
        browser.open('https://open.spotify.com/track/4u7EnebtmKWzUH433cf5Qv?si=7cdeea9d7a0c4572')


def previsao_tempo(tempo=False, minmax=False):
    site = get('http://api.openweathermap.org/data/2.5/weather?'
               'q=Itapecerica%20da%20serra,br&appid=ad48c1cc296b079ba845400c8b2a862a&units=metric&lang=pt')
    clima = site.json()
    # print(json.dumps(clima, indent=4))
    temperatura = clima['main']['temp']
    minima = clima['main']['temp_min']
    maxima = clima['main']['temp_max']
    descricao = clima['weather'][0]['description']
    if tempo:
        mensagem = f'No momento fazem {temperatura} graus com: {descricao}.'
        cria_audio(mensagem, 'tempo', '')
    if minmax:
        mensagem = f'Mínima de {minima} e máxima de {maxima}'
        cria_audio(mensagem, 'tempo', '')


def main():
    arq = 'audios/bem_vindo.mp3'
    executa_audio(arq)
    monitora_audio()

main()

"""AREA DE CRIAÇÃO DE AUDIOS"""
# cria_audio(f'Olá, Sou sua assistente. O que posso ajudar?', 'bem_vindo', '')
# cria_audio('um minuto por favor!', 'paciencia', '')