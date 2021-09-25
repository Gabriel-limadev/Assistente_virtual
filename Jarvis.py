import speech_recognition as sr

""" CONFIGURAÇÕES """
with open('jarvis-assistente-327121-994d1596bfa5.json') as credenciais_google:
    credenciais_google = credenciais_google.read()


def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        print("Aguardando o Comando:")
        audio = microfone.listen(source)

    try:
        print(microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-br'))
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))


monitora_audio()