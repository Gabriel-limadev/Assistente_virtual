from requests import get
from bs4 import BeautifulSoup
import webbrowser as browser
import paho.mqtt.client as mqtt
import platform
from gtts import gTTS  # Biblioteca principal de transformação de textos em audios
from subprocess import call  # biblioteca para executar o audio no MAC e LINUX
from playsound import playsound  #biblioteca para executar o audio no windows

""" CONFIGURAÇÕES """
hotword = 'assistente'


""" FUNÇÕES DE COMANDO """

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


def ultimas_noticias():
    site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419')
    noticias = BeautifulSoup(site.text, 'html.parser')
    n = 1
    for item in noticias.findAll('item')[:2]:
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


def publica_mqtt(cod):
    if cod == '1':
        mensagem = 'Luz ligada'
        cria_audio(mensagem, 'luz', '')
    if cod == '0':
        mensagem = 'Luz desligada'
        cria_audio(mensagem, 'luz', '')

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
        else:
            print("Connect returned result code: " + str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))

    # create the client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # enable TLS
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

    # set username and password
    client.username_pw_set("assistente", "Assistente2021")

    # connect to HiveMQ Cloud on port 8883
    client.connect("03de71e02afd4413b5c06f33ffe856bd.s1.eu.hivemq.cloud", 8883)

    # subscribe to the topic "my/test/topic"
    client.subscribe("my/test/topic")

    # publish "Hello" to the topic "my/test/topic"
    client.publish("my/test/topic", cod)

    # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
    client.loop_forever()


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
    elif 'liga a luz' in trigger:
        publica_mqtt('1')
    elif 'apaga a luz' in trigger:
        publica_mqtt('0')
    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem, 'repetir0', '')
        print('COMANDO INVÁLIDO', mensagem)
        executa_audio('audios/pagamento_invalido.mp3')

