from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from .llm import get_llm

class VerificationResult(BaseModel):
    is_correct: bool = Field(description="True if the solution is correct, False otherwise.")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0.")
    critique: str = Field(description="Explanation of any errors or confirmation of correctness.")
    correction: str = Field(description="If incorrect, provide the corrected final answer or step.")

class VerifierAgent:
    def __init__(self):
        self.llm = get_llm()
        self.parser = JsonOutputParser(pydantic_object=VerificationResult)
        
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are a strict Math Verifier.
            Review the problem and the proposed solution.
            
            Problem:
            {problem}
            
            Proposed Solution:
            {solution}
            
            Check for:
            1. Logical errors.
            2. Calculation mistakes.
            3. Unit consistency.
            4. Constraints violation.
            
            Format output as JSON.
            {format_instructions}
            """
        )
        self.chain = self.prompt | self.llm | self.parser

    def verify(self, problem_text: str, solution_text: str):
        return self.chain.invoke({
            "problem": problem_text,
            "solution": solution_text,
            "format_instructions": self.parser.get_format_instructions()
        })
