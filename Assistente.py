"""
Usarei o gtts - Google Text-to-Speech - Para transformar os textos em audios.
"""
import speech_recognition as sr
from funcoes_comandos import executa_audio, executa_comandos


hotword = 'assistente'
with open('jarvis-assistente-327121-994d1596bfa5.json') as credenciais_google:
    credenciais_google = credenciais_google.read()


""" FUNÇÃO PRINCIPAL """


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


def main():
    arq = 'audios/bem_vindo.mp3'
    executa_audio(arq)
    monitora_audio()


main()