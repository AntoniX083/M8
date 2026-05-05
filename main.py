import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import asyncio
from data import climate_terms
import random
import time
points = 0

def check_voice():
    duration = 5 # sekundy nagrania
    sample_rate = 44100

    print("🎙 Mów teraz...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("output2.wav", sample_rate, recording)
    print("✅ Nagrywanie zakończone, trwa rozpoznawanie...")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output2.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        print("📝 Powiedziałeś:", text)

        # Tłumaczenie tekstu
        translator = Translator()
        translated = asyncio.run(translator.translate(text, dest="pl")) # możesz zmienić język
        return translated.text

    except sr.UnknownValueError:
        print("😕 Mowa nie została rozpoznana.")
    except sr.RequestError as e:
        print(f"❗ Błąd usługi: {e}")

for i in range(3):
    random_phrase = random.choice(list(climate_terms.keys()))
    print("Przetłumacz na język angielski: " + random_phrase)
    time.sleep(2.5)
    user_voice = check_voice()
    if user_voice is not None and random_phrase.lower() == user_voice.strip().lower():
        print("Dobra odpowiedź")
        points += 1
    else:
        print("Zła odpowiedź")

    del climate_terms[random_phrase]

print("Zdobyte punkty: " + str(points))
