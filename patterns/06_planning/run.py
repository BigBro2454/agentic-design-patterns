import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    planner_prompt = ChatPromptTemplate.from_template(
        "You are an expert planner. Break down the following objective into a 3-step actionable plan.\n"
        "Objective: {objective}\n"
        "Output the plan as a numbered list."
    )
    planner_chain = planner_prompt | llm | StrOutputParser()
    
    executor_prompt = ChatPromptTemplate.from_template(
        "Execute the following step of a plan.\n"
        "Step: {step}\n"
        "Provide a concise summary of the execution result."
    )
    executor_chain = executor_prompt | llm | StrOutputParser()
    
    objective = "Launch a small email newsletter about AI."
    print(f"Objective: {objective}\n")
    print("Generating Plan...")
    plan_raw = planner_chain.invoke({"objective": objective})
    print(f"\nPlan:\n{plan_raw}\n")
    
    steps = [s.strip() for s in plan_raw.split("\n") if s.strip() and s[0].isdigit()]
    
    for i, step in enumerate(steps):
        print(f"Executing Step {i+1}...")
        result = executor_chain.invoke({"step": step})
        print(f"Result:\n{result}\n{'-'*40}\n")

if __name__ == "__main__":
    main()
