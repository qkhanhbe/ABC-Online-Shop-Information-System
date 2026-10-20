"""AI / application layer: speech-to-text.

SIMULATION: speech recognition is not performed. The "audio" passed in is already the
transcript a speech-to-text engine would return, so transcribe() only cleans it up.
A real engine (e.g. Whisper) can replace transcribe() without changing any caller.
"""


class SpeechService:

    def transcribe(self, audio_input):
        # Prototype: audio_input is already the transcribed text.
        return " ".join(str(audio_input).split())
