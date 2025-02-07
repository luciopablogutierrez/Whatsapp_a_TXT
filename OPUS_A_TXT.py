import os
import subprocess
import speech_recognition as sr

def opus_to_wav(opus_file, wav_file):
    """Convierte un archivo OPUS a WAV usando ffmpeg."""
    try:
        subprocess.run(["ffmpeg", "-i", opus_file, "-ac", "1", "-ar", "16000", wav_file], check=True)
        return wav_file
    except subprocess.CalledProcessError as e:
        print(f"Error al convertir OPUS a WAV: {e}")
        return None

def transcribe_audio(wav_file):
    """Transcribe el archivo WAV a texto usando SpeechRecognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="es-ES")  # Ajustá el idioma según necesites
        return text
    except sr.UnknownValueError:
        return "No se pudo reconocer el audio."
    except sr.RequestError as e:
        return f"Error en la API de reconocimiento: {e}"

def save_transcription(text, output_file):
    """Guarda el texto transcrito en un archivo .txt."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

def convert_opus_to_text(opus_file):
    """Convierte un archivo OPUS a texto plano y lo guarda en un archivo .txt."""
    wav_file = opus_file.replace(".opus", ".wav")
    txt_file = opus_file.replace(".opus", ".txt")

    if opus_to_wav(opus_file, wav_file):
        text = transcribe_audio(wav_file)
        save_transcription(text, txt_file)
        os.remove(wav_file)  # Borra el WAV después de la transcripción
        print(f"Transcripción guardada en {txt_file}")
        return txt_file
    return "Error en la conversión de OPUS a WAV."

# Uso
if __name__ == "__main__":
    opus_file = "audio.opus"  # Reemplazalo con el nombre de tu archivo OPUS
    convert_opus_to_text(opus_file)
