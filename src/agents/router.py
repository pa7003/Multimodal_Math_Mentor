from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from .llm import get_llm

class RoutingDecision(BaseModel):
    category: str = Field(description="The category of the math problem: 'algebra', 'calculus', 'probability', 'linear_algebra', 'other'.")
    complexity: str = Field(description="Estimated complexity: 'simple', 'medium', 'complex'.")
    recommended_tools: list[str] = Field(description="List of tools recommended (e.g., 'rag', 'calculator', 'python_repl').")

class IntentRouter:
    def __init__(self):
        self.llm = get_llm()
        self.parser = JsonOutputParser(pydantic_object=RoutingDecision)
        
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are an expert Math Tutor Router.
            Analyze the following parsed math problem and decide the best strategy.
            
            Problem Topic: {topic}
            Problem Text: {problem_text}
            
            Determine:
            1. Broad Category (map to: Algebra, Calculus, Probability, Linear Algebra, Other).
            2. Complexity (Simple calculation vs Multi-step reasoning).
            3. Recommended Tools (Always include 'rag' for formula retrieval. Use 'python_repl' for complex calculations).
            
            Format Instructions:
            {format_instructions}
            """
        )
        self.chain = self.prompt | self.llm | self.parser

    def route(self, problem_data: dict):
        return self.chain.invoke({
            "topic": problem_data.get("topic", "Unknown"),
            "problem_text": problem_data.get("problem_text", ""),
            "format_instructions": self.parser.get_format_instructions()
        })
