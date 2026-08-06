import os
import re
import shutil


class DirectoryManager:
    def __init__(self):
        self._directory = None

    def remove_a_dir(self, DIRECTORY : str = None):
        if not DIRECTORY:
            raise ValueError("No Directory Provided")
        if os.path.exists(DIRECTORY):
            shutil.rmtree(DIRECTORY)
            print(f"Directory {DIRECTORY} has been removed")
        else:
            print(f"Directory {DIRECTORY} does not exist")

    def save_to_dir(self, data : str, DIRECTORY : str, filename : str = "untitled.txt") -> str :
        try:
            os.makedirs(DIRECTORY, exist_ok=True)
            transcript_path = os.path.join(DIRECTORY, filename)
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(data)
            print(f"Transcript saved to {transcript_path}")
            return transcript_path
        except OSError as e:
            print(f"Failed to save transcript: {e}")
            raise

class Tools:
    def __init__(self):
        pass
    
    def clean_data(self, text: str) -> str:
          if not text:
            return ""
          
          text = re.sub(r"<[^>]+>", " ", text)
          text = re.sub(r"http\S+|www\.\S+", " ", text)
          text = re.sub(r"\S+@\S+", " ", text)
          text = re.sub(r"[#*_`~>]+", " ", text)
          text = re.sub(r"[^a-zA-Z0-9.,!?'\-\s]", " ", text)
          text = re.sub(r"([.\-]){2,}", r"\1", text)
          text = re.sub(r"\s+", " ", text)
          text = text.strip()
          text = text.replace("\n", " ")
          return text    