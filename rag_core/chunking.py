from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.logger import Logger
from utils.tools import Tools

class Chunking:
    def __init__(self):
        self.logger = Logger()
        self.log = self.logger.get_logger()
        self.tools = Tools()
        
    def chunking(self, raw_text : str, chunk_size : int = 900, chunk_overlap : int = 180) -> list:
        try:
            if not raw_text:
                return []
            clean_text = self.tools.clean_data(raw_text)
            if not clean_text:
                return []
            splitter = RecursiveCharacterTextSplitter(
                chunk_size = chunk_size,
                chunk_overlap = chunk_overlap,
                separators=["\n\n", "\n", ". ", " ", ""],
            )
            return splitter.split_text(clean_text)
        except Exception as e:
            self.log.error(f"Failed to chunk text: {e}")
            return []
