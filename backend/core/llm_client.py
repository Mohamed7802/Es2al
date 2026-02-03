"""
LLM client module.
Handles interaction with language models.
"""
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class LLMClient:
    """Handles LLM operations and prompt management."""
    
    DEFAULT_PROMPT_TEMPLATE = """
Answer the question based on the context below. If you can't 
answer the question, reply "I don't know".

Context: {context}

Question: {question}
"""
    
    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        api_key: str = None,
        temperature: float = 0.0,
        max_tokens: int = 1000
    ):
        """
        Initialize the LLM client.
        
        Args:
            model: OpenAI model name
            api_key: OpenAI API key
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.model = ChatOpenAI(
            openai_api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.parser = StrOutputParser()
        self.prompt = None
    
    def set_prompt_template(self, template: str = None) -> None:
        """
        Set the prompt template.
        
        Args:
            template: Prompt template string (uses default if None)
        """
        template = template or self.DEFAULT_PROMPT_TEMPLATE
        self.prompt = ChatPromptTemplate.from_template(template)
    
    def generate(self, prompt_vars: dict) -> str:
        """
        Generate a response using the LLM.
        
        Args:
            prompt_vars: Variables to fill the prompt template
            
        Returns:
            Generated response string
        """
        if self.prompt is None:
            self.set_prompt_template()
        
        chain = self.prompt | self.model | self.parser
        return chain.invoke(prompt_vars)
    
    def get_model(self):
        """Get the underlying model for chain integration."""
        return self.model
    
    def get_prompt(self):
        """Get the prompt template for chain integration."""
        if self.prompt is None:
            self.set_prompt_template()
        return self.prompt
    
    def get_parser(self):
        """Get the output parser for chain integration."""
        return self.parser