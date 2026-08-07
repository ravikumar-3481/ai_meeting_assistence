from langchain_core.messages import HumanMessage, AIMessage
from utils.logger import Logger
import re
from agent.agent_core import MeetingAgent
from rag_core.rag_pipline import RagPipeline

log = Logger().get_logger()
rag = RagPipeline()

def main(url : str, language : str = "english"):
    MAX_HISTORY_TURNS = 6
    meeting_id , title = rag.rag_pipeline(url, language=language)
    log.info(f"[bold cyan]Active meeting ID: {meeting_id}[/bold cyan]\n")  
    log.info(f"[bold green]Active meeting : {title}[/bold green]\n") 

    agent = MeetingAgent(verbose=False)  
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