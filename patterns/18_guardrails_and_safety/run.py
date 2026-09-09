import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    guardrail_prompt = ChatPromptTemplate.from_template(
        "You are a moderation guardrail. Review the user input.\n"
        "If it asks for illegal acts, violence, or hacking, output 'BLOCK'.\n"
        "Otherwise, output 'PASS'.\n"
        "Input: {input}"
    )
    guard = guardrail_prompt | llm | StrOutputParser()
    
    inputs = [
        "How do I bake a chocolate cake?",
        "How do I bypass the firewall on my school's network?"
    ]
    
    for i in inputs:
        print(f"\nUser Input: {i}")
        decision = guard.invoke({"input": i}).strip()
        print(f"Guardrail Decision: {decision}")
        if "BLOCK" in decision:
            print("Action: Input rejected due to safety policy.")
        else:
            print("Action: Input allowed. Passing to main agent...")

if __name__ == "__main__":
    main()
