import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import time
import threading

# --- INITIALIZATION ---
# Initialize the engine and recognizer globally
engine = pyttsx3.init()
recognizer = sr.Recognizer()


def run_speak(text, engine):
    """
    Helper function to run the pyttsx3 commands. 
    It is defined globally so threading.Thread can easily find it.
    """
    try:
       
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 170)
        
        engine.say(text)
        engine.runAndWait()
        
        # Reset rate
        engine.setProperty('rate', rate)
    except Exception as e:
        # This catches errors that occur inside the thread
        print(f"Speech Thread Error: {e}")

# --- REVISED SPEAK FUNCTION ---
def speak(text):
    """
    Function to initiate text-to-speech output in a separate thread.
    This prevents the speech from blocking the main microphone listening loop.
    """
    # Start the speech process in a new thread, pointing the target to run_speak
    speech_thread = threading.Thread(
        target=run_speak,
        # Pass the text to speak and the global engine object to the run_speak function
        args=(text, engine) 
    )
    speech_thread.start()

# --- GREETING FUNCTION ---
def greet():
    """Returns a time-appropriate greeting."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good morning sir, how can I help you today!"
    elif 12 <= hour < 18:
        return "Good afternoon sir, how can I help you today!"
    else:
        return "Good evening sir, how can I help you today!"
    
# --- COMMAND PROCESSING FUNCTION ---
def processcommand(c):
    """Processes the voice command and performs an action."""
    c_lower = c.lower()
    
    if "open google" in c_lower:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in c_lower:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c_lower:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c_lower:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif "open github" in c_lower:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")
    elif "what time is it" in c_lower:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Sir, the current time is {current_time}")
    elif "exit" in c_lower or "quit" in c_lower or "stop listening" in c_lower:
        speak("Goodbye, sir. Shutting down.")
        # Raise an exception to cleanly break the while loop
        raise SystemExit 
    else:
        speak("Sorry, I didn't recognize that command.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    speak("Initializing Jarvis.......")
    speak(greet())
    
    while True:
        try:
            #  LISTENING FOR WAKE WORD ---
            with sr.Microphone() as source:
                print("Listening for 'Jarvis'...")
                # Reduce background noise
                recognizer.adjust_for_ambient_noise(source, duration=1) 

                # Use adjusted time limits
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
            word = recognizer.recognize_google(audio)
            print("You said:", word)
            
            # WORD CHECK ---
            if "jarvis" in word.lower():
                speak("Yes sir. How can I help you?") 
                
                # LISTENING FOR COMMAND ---
                with sr.Microphone() as source:
                    print("Jarvis Active. Listening for command...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5) 
                    
                    audio = recognizer.listen(source, phrase_time_limit=8)
                    command = recognizer.recognize_google(audio)
                    print("Command:", command)
                    
                    # --- PROCESS COMMAND ---
                    processcommand(command)
                    
        # --- EXCEPTION HANDLING ---
        except sr.WaitTimeoutError:
            # Handles silence or timeout during wake word listening
            continue
        except sr.UnknownValueError:
            # Handles speech that couldn't be transcribed
            print("Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            # Handles connection or API errors
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except SystemExit:
            # Handles clean exit triggered by 'exit' command
            break
        except Exception as e:
            # Catch all other unexpected errors
            print(f"An unexpected error occurred: {e}")