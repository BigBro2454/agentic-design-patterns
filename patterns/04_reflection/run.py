import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    generator_prompt = ChatPromptTemplate.from_template(
        "Write a 2-sentence marketing pitch for a new smart coffee mug.\n"
        "Feedback from previous attempt (if any): {feedback}\n"
        "Pitch:"
    )
    generator_chain = generator_prompt | llm | StrOutputParser()
    
    critic_prompt = ChatPromptTemplate.from_template(
        "Review the following marketing pitch for a smart coffee mug.\n"
        "Does it mention the 'temperature control' feature explicitly? Is it under 3 sentences?\n"
        "If it meets the criteria, output 'APPROVED'.\n"
        "If not, provide short constructive feedback on what needs to change.\n"
        "Pitch: {pitch}"
    )
    critic_chain = critic_prompt | llm | StrOutputParser()
    
    feedback = "None"
    max_iterations = 3
    
    for i in range(max_iterations):
        print(f"\n--- Iteration {i+1} ---")
        pitch = generator_chain.invoke({"feedback": feedback})
        print(f"Generator:\n{pitch}")
        
        evaluation = critic_chain.invoke({"pitch": pitch})
        print(f"Critic:\n{evaluation}")
        
        if "APPROVED" in evaluation.upper():
            print("\n✅ Final approved pitch achieved!")
            break
        else:
            feedback = evaluation

if __name__ == "__main__":
    main()
