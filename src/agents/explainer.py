from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .llm import get_llm

class ExplainerAgent:
    def __init__(self):
        self.llm = get_llm()
        
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are a kind and patient Math Tutor.
            Your goal is to explain the solution to a student clearly.
            
            Problem:
            {problem}
            
            Technical Solution:
            {solution}
            
            Instructions:
            1. Break down the logic in simple terms.
            2. Explain WHY each step was taken.
            3. Mention any formulas used.
            4. Be encouraging.
            5. If there are citations/sources, mention them briefly as "Reference".
            """
        )
        self.chain = self.prompt | self.llm | StrOutputParser()

    def explain(self, problem_text: str, solution_text: str, citations: list = []):
        return self.chain.invoke({
            "problem": problem_text,
            "solution": solution_text
        })
