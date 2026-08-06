from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from agent.prompts.system_prompt import SystemPrompt
from llm.llm_model import LLM
from utils.logger import Logger
from agent.tools import ALL_TOOLS


SYSTEM_PROMPT = SystemPrompt().System_Prompt()

class MeetingAgent:
    def __init__(self):
        self.log = Logger().get_logger()
        self.llm = LLM().get_llm(temperature=0.1)
        self.tools = ALL_TOOLS
        self.executor = self._build_executor()

    def _build_executor(self) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ])
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,           # set False once you trust it, keeps logs quieter
            handle_parsing_errors=True,
        )

    def run(self, user_input: str, chat_history: list | None = None) -> str:
        try:
            result = self.executor.invoke({
                "input": user_input,
                "chat_history": chat_history or [],
            })
            return result["output"]
        except Exception as e:
            self.log.error(f"Agent execution failed: {e}")
            return f"Something went wrong while handling that: {e}"