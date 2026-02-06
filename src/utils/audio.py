import whisper
import tempfile
import os

class AudioProcessor:
    def __init__(self, model_size="base"):
        # Load whisper model
        # Available models: tiny, base, small, medium, large
        print(f"Loading Whisper model: {model_size}...")
        self.model = whisper.load_model(model_size)

    def process_audio(self, audio_bytes):
        """
        Process audio bytes and return text transcription.
        """
        try:
            # Whisper requires a file path usually, or specific handling
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_path = tmp_file.name

            # Transcribe
            result = self.model.transcribe(tmp_path)
            
            # Cleanup
            os.remove(tmp_path)
            
            return {
                "text": result["text"],
                "language": result.get("language", "unknown")
            }
        except Exception as e:
            return {
                "text": "",
                "error": str(e)
            }
