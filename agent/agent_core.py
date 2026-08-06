from langchain.agents import create_agent
from agent.prompts.system_prompt import SystemPrompt
from llm.llm_model import LLM
from utils.logger import Logger
from agent.tools import ALL_TOOLS
from agent.agent_tools import ADVANCED_TOOLS


SYSTEM_PROMPT = SystemPrompt().System_Prompt()


class MeetingAgent:

    def __init__(self, verbose: bool = False):
        self.log = Logger().get_logger()
        self.llm = LLM().get_llm(temperature=0.1)
        self.tools = ALL_TOOLS + ADVANCED_TOOLS
        self.verbose = verbose

        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
        )

    def run(self, user_input: str, chat_history: list | None = None) -> str:
        
        try:
            messages = list(chat_history or [])
            messages.append(("human", user_input))

            result = self.agent.invoke({"messages": messages})

            final_message = result["messages"][-1]
            content = getattr(final_message, "content", None)

            if self.verbose:
                self.log.info(f"Full message trace: {result['messages']}")

            return content if content else "The agent didn't return a response for that."
        except Exception as e:
            self.log.error(f"Agent execution failed: {e}")
            return f"Something went wrong while handling that: {e}"