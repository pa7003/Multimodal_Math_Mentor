from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .llm import get_llm
import sys
import os

# Adjust path for RAG import if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.rag.store import RAGStore

class SolverAgent:
    def __init__(self):
        self.llm = get_llm()
        self.rag = RAGStore()
        
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are an expert Math Solver.
            Solve the given problem step-by-step.
            
            Use the following retrieved context (formulas/examples) to ensure accuracy:
            {context}
            
            Problem:
            {problem}
            
            Constraints:
            {constraints}
            
            Instructions:
            1. State the relevant formula(s) from context.
            2. Show detailed steps.
            3. Final Answer should be clearly boxed or stated.
            """
        )
        self.chain = self.prompt | self.llm | StrOutputParser()

    def solve(self, problem_data: dict):
        # Retrieve context
        problem_text = problem_data.get("problem_text", "")
        topic = problem_data.get("topic", "")
        
        # Combine text and topic for better retrieval
        query = f"{topic}: {problem_text}"
        
        # 1. Check Memory first
        memory_context = ""
        try:
            mem_docs = self.rag.retrieve_memory(query, k=1)
            if mem_docs:
                memory_context = f"\n[SIMILAR PAST PROBLEM]:\n{mem_docs[0].page_content}\n"
        except Exception:
            pass # No memory yet
            
        try:
            docs = self.rag.retrieve(query, k=2)
            context = "\n\n".join([d.page_content for d in docs])
            citations = [d.metadata.get("source", "unknown") for d in docs]
        except Exception as e:
            context = "No context available (Retrieval Error)."
            citations = []
            
        # Combine Memory + Knowledge Base
        full_context = f"{memory_context}\n\n[KNOWLEDGE BASE]:\n{context}"
            
        solution = self.chain.invoke({
            "context": full_context,
            "problem": problem_text,
            "constraints": ", ".join(problem_data.get("constraints", []))
        })
        
        return {
            "solution": solution,
            "context_used": full_context,
            "citations": citations
        }

    def learn(self, problem_text, solution_text, topic):
        try:
            self.rag.add_to_memory(problem_text, solution_text, topic)
            return True
        except Exception as e:
            print(f"Memory Error: {e}")
            return False
