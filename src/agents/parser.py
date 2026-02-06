from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import List, Optional
from .llm import get_llm

class MathProblem(BaseModel):
    problem_text: str = Field(description="The clean, extracted math problem text.")
    topic: str = Field(description="The mathematical topic (e.g., Algebra, Calculus, Probability).")
    subtopic: Optional[str] = Field(description="Specific subtopic if applicable.")
    variables: List[str] = Field(description="List of identified variables.")
    constraints: List[str] = Field(description="List of explicit or implicit constraints (e.g., x > 0).")
    needs_clarification: bool = Field(description="True if the input is ambiguous or missing information, else False.")
    clarification_question: Optional[str] = Field(description="Question to ask user if needs_clarification is True.")

class ParserAgent:
    def __init__(self):
        self.llm = get_llm()
        self.parser = JsonOutputParser(pydantic_object=MathProblem)
        
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are a rigorous Math Problem Parser.
            Your task is to convert raw, potentially messy text (from OCR/Speech) into a structured math problem object.
            
            Analyze the input for:
            1. Core problem statement (clean up typos).
            2. Mathematical Topic (Algebra, Probability, Calculus, Linear Algebra).
            3. Variables and Constraints.
            4. AMBIGUITY: If the problem is missing AMBIGUOUS or INCOMPLETE information (e.g. "Solve for x" but no equation, or "Find the limit" but no function), set 'needs_clarification' to True and generate a specific question.
            
            Input Text:
            {input_text}
            
            Format Instructions:
            {format_instructions}
            """
        )
        
        self.chain = self.prompt | self.llm | self.parser

    def parse(self, text: str):
        try:
            return self.chain.invoke({
                "input_text": text,
                "format_instructions": self.parser.get_format_instructions()
            })
        except Exception as e:
            return {
                "problem_text": text,
                "needs_clarification": True,
                "clarification_question": f"Parsing failed. Error: {str(e)}. Please clean up the text.",
                "topic": "Unknown",
                "variables": [],
                "constraints": []
            }
