from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from llm.llm_model import LLM
from llm.prompts import Prompts
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