"""
Usarei o gtts - Google Text-to-Speech - Para transformar os textos em audios.
"""
import speech_recognition as sr
from gtts import gTTS  # Biblioteca principal de transformação de textos em audios
import platform
from subprocess import call  # biblioteca para executar o audio no MAC e LINUX
from playsound import playsound  #biblioteca para executar o audio no windows

"""Criação e execução de audios"""


def cria_audio(texto, nome):
    tts = gTTS(texto, lang='pt-br', slow=False)
    arq = 'audios/' + nome
    tts.save(arq)
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
        arq = 'audios/bem_vindo.mp3'
        executa_audio(arq)
        while True:
            print("Aguardando o Comando:")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-br')
                trigger = trigger.lower()
                if hotword in trigger:
                    print('Comando: ', trigger)
                    arq = 'audios/audio.mp3'
                    executa_audio(arq)
                    """ executar os comandos """
                    break

            except sr.UnknownValueError:
                print("Google Cloud Speech could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger


"""AREA DE CRIAÇÃO DE AUDIOS"""
#cria_audio(f'Seja bem vindo {platform.node()}', 'bem_vindo.mp3')
# cria_audio('só um minuto', )


def main():
    monitora_audio()

main()







