import speech_recognition as sr
from pydub import AudioSegment
import os

def transcribe_audio(audio_path):
    """
    Transcribe audio file to text using Google Speech Recognition
    
    Args:
        audio_path (str): Path to audio file
        
    Returns:
        str: Transcribed text or None if failed
    """
    try:
        # Convert audio to WAV format if needed
        audio = AudioSegment.from_file(audio_path)
        wav_path = audio_path.replace(os.path.splitext(audio_path)[1], '.wav')
        audio.export(wav_path, format='wav')
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Load audio file
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            
        # Transcribe using Google Speech Recognition
        text = recognizer.recognize_google(audio_data)
        
        # Clean up temporary WAV file
        if os.path.exists(wav_path) and wav_path != audio_path:
            os.remove(wav_path)
        
        return text
        
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None
