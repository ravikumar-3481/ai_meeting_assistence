import os
import json
import requests
from deepgram import DeepgramClient
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from api.config import Config
from utils.logger import Logger
from audio.audio_processor import AudioProcessor
from utils.tools import DirectoryManager


class Transcriber:
    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.directory_manager = DirectoryManager()
        self.logger = Logger().get_logger()
        self.config = Config()
        self.SARVAM_API_KEY = self.config.sarvam_api_key.get_secret_value()
        self.SARVAM_STT_TRANSLATE_URL = self.config.sarvam_stt_translate_url
        self.SARVAM_MODEL = self.config.sarvam_model
        self.api_key = self.config.deepgram_api_key.get_secret_value()
        self._client = None

    def get_client(self) -> DeepgramClient:
        if self._client is None:
            if not self.api_key:
                raise ValueError("DEEPGRAM_API_KEY is not set")
            self._client = DeepgramClient(api_key=self.api_key)
        return self._client

    def transcribe_chunk_deepgram(self, chunk_path: str, translate: bool = False) -> str:
        try:
            client = self.get_client()
        except Exception as e:
            self.logger.error(f"Deepgram client unavailable: {e}")
            return ""

        try:
            with open(chunk_path, "rb") as audio:
                buffer_data = audio.read()
        except (FileNotFoundError, OSError) as e:
            self.logger.error(f"Could not read audio chunk {chunk_path}: {e}")
            return ""

        kwargs = {"model": "nova-3", "smart_format": True}
        if translate:
            kwargs["detect_language"] = True

        try:
            response = client.listen.v1.media.transcribe_file(request=buffer_data, **kwargs)
            return response.results.channels[0].alternatives[0].transcript
        except (AttributeError, IndexError, KeyError) as e:
            self.logger.error(f"Unexpected Deepgram response format for {chunk_path}: {e}")
            return ""
        except Exception as e:
            self.logger.error(f"Deepgram transcription failed for {chunk_path}: {e}")
            return ""

    def transcribe_chunk_sarvam(self, chunk_path: str) -> str:
        if not self.SARVAM_API_KEY:
            self.logger.info("SARVAM_API_KEY is not set. Shifting to Deepgram.")
            return self.transcribe_chunk_deepgram(chunk_path)

        headers = {"api-subscription-key": self.SARVAM_API_KEY}
        data = {"model": self.SARVAM_MODEL, "with_diarization": "false"}

        try:
            with open(chunk_path, "rb") as audio:
                files = {"file": (os.path.basename(chunk_path), audio, "audio/wav")}
                response = requests.post(
                    self.SARVAM_STT_TRANSLATE_URL,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=300,
                )
            response.raise_for_status()
        except (FileNotFoundError, OSError) as e:
            self.logger.error(f"Could not read audio chunk {chunk_path}: {e}")
            return ""
        except requests.exceptions.Timeout:
            self.logger.error(f"Sarvam request timed out for {chunk_path}")
            return ""
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Sarvam request failed for {chunk_path}: {e}")
            return ""

        try:
            return response.json().get("transcript", "")
        except (json.JSONDecodeError, ValueError, AttributeError) as e:
            self.logger.error(f"Could not parse Sarvam response for {chunk_path}: {e}")
            return ""

    def transcribe(self, chunks: list, language: str = "english") -> str:
        engine = "Sarvam Ai" if language.lower() == "hinglish" else "Deepgram"
        self.logger.info(f"\nUsing [bold cyan]{engine}[/bold cyan] for transcription...\n")

        full_transcribe = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ) as progress:
            task = progress.add_task("[yellow]Transcribing...", total=len(chunks))

            for i, chunk in enumerate(chunks):
                progress.update(task, description=f"[cyan]Transcribing Chunk {i + 1}/{len(chunks)}...")
                try:
                    if language.lower() == "hinglish":
                        text = self.transcribe_chunk_sarvam(chunk)
                    else:
                        text = self.transcribe_chunk_deepgram(chunk, translate=True)
                except Exception as e:
                    self.logger.error(f"Error occurred while transcribing chunk {chunk}: {e}")
                    text = ""

                full_transcribe.append(text)
                progress.advance(task)

        self.logger.info("[bold green]✔ Transcription Complete![/bold green]\n")
        self.directory_manager.remove_a_dir("data/downloads")
        return "\n".join(full_transcribe) + "\n"