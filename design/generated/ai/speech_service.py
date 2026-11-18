from __future__ import annotations



class SpeechService:

    def transcribe(self, audio_input: str) -> str:
        raise NotImplementedError

    def transcribe_audio(self, path: str) -> str:
        raise NotImplementedError

    def load(self) -> WhisperModel:
        raise NotImplementedError
