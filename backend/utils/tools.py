import os
import re
import uuid
import datetime
import shutil
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from llm.llm_model import LLM
from utils.logger import Logger


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
        self.llm = LLM()
        self.log = Logger().get_logger()
    
    def clean_data(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"http\S+|www\.\S+", " ", text)
        text = re.sub(r"\S+@\S+", " ", text)
        text = re.sub(r"[#*_`~>]+", " ", text)
        # Remove control characters while preserving alphanumeric, punctuation, spaces, and all unicode letters/words
        text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", " ", text)
        text = re.sub(r"([.\-]){2,}", r"\1", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _title_prompt(self) -> str:
        return """
        You generate a short title for a meeting, the way a chat app names a
        conversation thread.

        Rules:
        - Exactly 3 to 4 words. Not 2, not 5.
        - Plain words describing what the meeting was actually about.
        - No punctuation, no quotes, no colons, no trailing period.
        - No generic filler like "Team Meeting" or "General Discussion" unless
          the content genuinely gives you nothing more specific.
        - Return ONLY the title. No explanation, no formatting, nothing else.

        Meeting content:
        {context}
        """

    def generate_meeting_title(self, context: str) -> str:
        """Ask the LLM for a short 3-4 word meeting title based on transcript content."""
        if not context or not context.strip():
            return "Untitled Meeting"

        try:
            llm = self.llm.get_llm(temperature=0.4)
            prompt_template = ChatPromptTemplate.from_template(self._title_prompt())
            chain = prompt_template | llm | StrOutputParser()

            # First ~1500 chars is enough context for a title, keeps this call cheap
            trimmed_context = context[:1500]
            title = chain.invoke({"context": trimmed_context})
            title = title.strip().strip('"').strip("'").rstrip(".")

            words = title.split()
            if not words:
                return "Untitled Meeting"
            if len(words) > 4:
                title = " ".join(words[:4])

            return title or "Untitled Meeting"
        except Exception as e:
            self.log.warning(f"Meeting title generation failed, falling back: {e}")
            return "Untitled Meeting"

    def generate_meeting_id(self, context: str = "") -> tuple[str, str]:
        title = self.generate_meeting_title(context)
        date_tag = datetime.date.today().strftime("%Y%m%d")
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-").lower()
        slug = slug or "meeting"
        short_uuid = uuid.uuid4().hex[:6]
        meeting_id = f"{date_tag}-{slug}-{short_uuid}"

        return meeting_id, title