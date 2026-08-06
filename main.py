from langchain_core.messages import HumanMessage, AIMessage
from utils.logger import Logger
import re
from rag_core.chunking import Chunking
from rag_core.embedding import Embeddings
from agent.tools import set_session_transcript
from agent.agent_core import MeetingAgent

log = Logger().get_logger()

TRANSCRIPT_PATH = "data/transcripts/transcript.txt"
CHUNK_SIZE = 900
CHUNK_OVERLAP = 180
MAX_HISTORY_TURNS = 6  # keep last N human/AI turns so the prompt doesn't grow forever


def load_transcript(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().replace("\n", " ").replace("\r", " ").strip()


def prepare_session() -> None:
    log.info("Loading transcript...\n")
    transcript = load_transcript(TRANSCRIPT_PATH)
    if not transcript:
        raise ValueError(f"Transcript at '{TRANSCRIPT_PATH}' is empty or missing.")

    chunking = Chunking()
    embedding = Embeddings()

    chunks = chunking.chunking(transcript, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    log.info(f"Total chunks created: {len(chunks)}\n")
    if not chunks:
        raise ValueError("Chunking produced 0 chunks — check the transcript content.")

    embedding_vector = embedding.embed_batch(chunks)
    log.info(f"Embeddings ready for {len(chunks)} chunks "
              f"({len(embedding_vector[0])} dimensions).\n")

    set_session_transcript(chunks, embedding_vector)
    log.info("Session ready. The agent can now search, summarize, and generate "
              "action items / minutes / follow-up emails for this meeting.\n")


def main():
    prepare_session()

    agent = MeetingAgent(verbose=False)  # flip to True if you want to see tool-selection reasoning
    chat_history: list = []

    log.info("[bold green]Agent ready.[/bold green] Ask anything about the meeting "
              "(type 'exit' to quit).\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue

        answer = agent.run(question, chat_history=chat_history)
        answer = re.sub(r"^\s+|\s+$", "", answer).strip()
        print(f"\nAgent: {answer}\n")

        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=answer))
        chat_history = chat_history[-(MAX_HISTORY_TURNS * 2):]


if __name__ == "__main__":
    main()