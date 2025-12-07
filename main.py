#PIP PACKAGES 

import speech_recognition as sr
import webbrowser
import pyttsx3
from openai import OpenAI
import pyaudio
import os

# Initializing the recognizer 
r = sr.Recognizer() 

# Function to convert text to speech 

def Speak(command):
    
    # Initializing the engine
    
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()


client = OpenAI(
    api_key="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")

def aiProcess(command):
    
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",  
        messages=[
            {"role": "system", "content": "AI assistant named jarvis"},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content


def process_command(c):
    if "open google" in c.lower():
        Speak("Opening Google")
        webbrowser.open("https://www.google.com")
        
    elif "open facebook" in c.lower():
        Speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
        
    elif "open youtube" in c.lower():
        Speak("Opening Youtube")
        webbrowser.open("https://youtube.com")
        
    elif "open linkedin" in c.lower():
        Speak("Opening linkedin")
        webbrowser.open("https://linkedin.com")
        
    elif "open github" in c.lower():
        Speak("Opening Github")
        webbrowser.open("https://github.com")   
        
    else:
        output = aiProcess(c)    
        Speak(output)




#MAIN FUNCTION 
if __name__ == "__main__":
    Speak("Initializing Orion....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
            word = r.recognize_google(audio)
            print("you said:",word)
            if(word.lower() == "Orion"):
                Speak("Yes sir")
                # Listen for command
                with sr.Microphone() as source:
                    print("Orion Active...")
                    r.adjust_for_ambient_noise(source)# REDUCES BACKGROUND NOISE
                    command = r.recognize_google(audio)
                    
                    
                    process_command(command)

                   

        except Exception as e:
            print("Error; {0}".format(e))

        