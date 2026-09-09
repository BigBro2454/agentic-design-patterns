import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    goal_monitor_prompt = ChatPromptTemplate.from_template(
        "You are a Goal Monitor. The main goal is: {goal}\n"
        "Current state: {current_state}\n"
        "Calculate a progress percentage (0-100) and state what needs to happen next.\n"
        "Format: Progress: [X]% | Next: [Action]"
    )
    monitor_chain = goal_monitor_prompt | llm | StrOutputParser()
    
    goal = "Write a 3-chapter short story."
    
    states = [
        "Started a blank document.",
        "Finished drafting Chapter 1 and outlining Chapter 2.",
        "Completed all 3 chapters and ran a spell check."
    ]
    
    print(f"Tracking Goal: {goal}\n")
    for state in states:
        print(f"Event: {state}")
        status = monitor_chain.invoke({"goal": goal, "current_state": state})
        print(f"Monitor: {status.strip()}\n")

if __name__ == "__main__":
    main()
