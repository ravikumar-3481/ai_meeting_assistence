from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agent.prompts.agent_prompts import AdvancedPrompts
from langchain_core.runnables import RunnablePassthrough
from llm.llm_model import LLM
from llm.prompts.prompts import Prompts
from rag_core.chunking import Chunking
from utils.logger import Logger
import re



class Models:

    def __init__(self):
        self.llm = LLM()
        self.prompts = Prompts()
        self.chunking = Chunking()
        self.log = Logger().get_logger()

        
    def _build_chain(self, system_prompt: str):
        llm = self.llm.get_llm()
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_prompt), ("human", "{text}")]
        )
        return (
            {"text": RunnablePassthrough()}
            | prompt_template
            | llm
            | StrOutputParser()
        )
    
    def generate_discussion_topics(self, context: str) -> str:
        if not context:
            self.log.warning("Missing context for discussion topic generation")
            return ""
    
        try:
            llm = self.llm.get_llm(temperature=0.1)
            prompt_template = ChatPromptTemplate.from_template(self.prompts.rag_assist())
            chain = prompt_template | llm | StrOutputParser()
    
            response = chain.invoke({"context": context})
            response = re.sub(r"^\s+|\s+$", "", response)
            return response.strip()
    
        except Exception as e:
            self.log.error(f"Failed to generate key information: {e}")
            raise RuntimeError(f"Failed to Generate Key Information: {e}") from e

    def generate_answers(self, context: str, question: str) -> str:
        if not context or not question:
            self.log.warning("Missing context or question for answer generation")
            return ""
    
        try:
            llm = self.llm.get_llm(temperature=0.1)
            prompt_template = ChatPromptTemplate.from_template("you are a helpful assistant. Use the following context to answer the question.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:")
            chain = prompt_template | llm | StrOutputParser()
    
            response = chain.invoke({"context": context, "question": question})
            response = re.sub(r"^\s+|\s+$", "", response)
            return response.strip()
    
        except Exception as e:
            self.log.error(f"Failed to generate answers: {e}")
            raise RuntimeError(f"Failed to Generate Answers: {e}") from e




class AdvancedModels:
    def __init__(self):
        self.llm = LLM()
        self.prompts = AdvancedPrompts()
        self.log = Logger().get_logger()

    def _run(self, prompt_text: str, context: str) -> str:
        if not context:
            self.log.warning("Missing context for generation")
            return ""
        try:
            llm = self.llm.get_llm(temperature=0.1)
            prompt_template = ChatPromptTemplate.from_template(prompt_text)
            chain = prompt_template | llm | StrOutputParser()
            response = chain.invoke({"context": context})
            return re.sub(r"^\s+|\s+$", "", response).strip()
        except Exception as e:
            self.log.error(f"Generation failed: {e}")
            raise RuntimeError(f"Generation failed: {e}") from e

    def generate_action_items(self, context: str) -> str:
        return self._run(self.prompts.action_items_prompt(), context)

    def generate_meeting_minutes(self, context: str) -> str:
        return self._run(self.prompts.meeting_minutes_prompt(), context)

    def generate_followup_email(self, context: str) -> str:
        return self._run(self.prompts.followup_email_prompt(), context)

    def generate_open_questions(self, context: str) -> str:
        return self._run(self.prompts.open_questions_prompt(), context)

    def generate_tension_points(self, context: str) -> str:
        return self._run(self.prompts.tension_points_prompt(), context)