import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import asyncio

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
    text = recognizer.recognize_google(audio, language="pl-PL")
    print("📝 Powiedziałeś:", text)

    # Tłumaczenie tekstu
    translator = Translator()
    translated = asyncio.run(translator.translate(text, dest="en")) # możesz zmienić język
    print("🌍 Tłumaczenie na angielski:", translated.text)

except sr.UnknownValueError:
    print("😕 Mowa nie została rozpoznana.")
except sr.RequestError as e:
    print(f"❗ Błąd usługi: {e}")