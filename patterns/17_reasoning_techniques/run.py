import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    # Chain of Thought (CoT) pattern
    cot_prompt = ChatPromptTemplate.from_template(
        "Solve the following logic puzzle.\n"
        "Puzzle: {puzzle}\n"
        "Let's think step by step before giving the final answer."
    )
    cot_chain = cot_prompt | llm | StrOutputParser()
    
    puzzle = "I have a 5-liter jug and a 3-liter jug, and an unlimited supply of water. How do I measure exactly 4 liters?"
    print("Puzzle:", puzzle)
    print("\nExecuting Chain of Thought Reasoning...")
    
    response = cot_chain.invoke({"puzzle": puzzle})
    print("\nReasoning & Answer:\n", response)

if __name__ == "__main__":
    main()
