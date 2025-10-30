# audio_utils.py
import tempfile
import soundfile as sf
import whisper

def transcribe_audio(audio):
    """
    Handles both recorded (numpy) and uploaded (filepath) audio.
    Converts to WAV and transcribes using Whisper.
    """
    if audio is None:
        raise ValueError("❌ No audio received. Please record or upload a file.")

    model = whisper.load_model("base")

    # Case 1: User uploads a file → audio is a string (file path)
    if isinstance(audio, str):
        result = model.transcribe(audio)
        return result["text"]

    # Case 2: User records audio → audio is a tuple (data, samplerate)
    elif isinstance(audio, tuple) and len(audio) == 2:
        data, samplerate = audio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            sf.write(tmpfile.name, data, samplerate)
            tmpfile.flush()
            result = model.transcribe(tmpfile.name)
            return result["text"]

    else:
        raise ValueError(f"Unexpected audio type: {type(audio)} with length {len(audio) if hasattr(audio, '__len__') else 'N/A'}")
