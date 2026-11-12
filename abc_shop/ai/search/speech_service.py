"""AI / application layer: speech-to-text.

Two ways in, one result (a cleaned transcript):
  * transcribe_audio(path): real speech recognition of a recording made in the browser, with the
    offline Whisper model tiny.en (faster-whisper, int8 on the CPU, about 75 MB). The model is
    downloaded once into data/stt_model and loaded on first use.
  * transcribe(text): the typed "voice transcript" of the prototype; kept for tests, the terminal
    demo and machines without the model.
"""
import os
import re
import threading

MODEL_NAME = "tiny.en"
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                         "data", "stt_model")


class SpeechUnavailable(RuntimeError):
    pass


class SpeechService:

    def __init__(self):
        self._model = None
        self._lock = threading.Lock()

    def transcribe(self, audio_input):
        # Typed transcript: only normalise the spacing.
        return " ".join(str(audio_input).split())

    def load(self):
        """Load the Whisper model (downloads it the first time)."""
        with self._lock:
            if self._model is None:
                try:
                    from faster_whisper import WhisperModel
                except ImportError as e:
                    raise SpeechUnavailable("speech recognition needs: pip install faster-whisper") from e
                self._model = WhisperModel(MODEL_NAME, device="cpu", compute_type="int8", download_root=MODEL_DIR)
        return self._model

    def transcribe_audio(self, path):
        """Recognise the speech in an audio file (webm, ogg, wav, mp3...) and return the text."""
        segments, _ = self.load().transcribe(path, language="en", beam_size=1, vad_filter=True,
                                             initial_prompt="Shopping search: shoes, bags, shirts, caps, watches, orders.")
        text = " ".join(s.text for s in segments)
        text = re.sub(r"\$\s?(\d+)", r"\1 dollars", text)          # "$150" -> "150 dollars" for the price filter
        text = re.sub(r"(?<=\d),(?=\d{3})", "", text)                # "1,000" -> "1000"
        return " ".join(re.sub(r"[.,?!;:]", " ", text).split()).lower()
