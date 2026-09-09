import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    eval_prompt = ChatPromptTemplate.from_template(
        "Evaluate the assistant's response on a scale of 1 to 5 for Helpfulness and Tone.\n"
        "User: {user}\nAssistant: {assistant}\n"
        "Format: Helpfulness: [1-5], Tone: [1-5], Notes: [brief reason]"
    )
    evaluator = eval_prompt | llm | StrOutputParser()
    
    user_msg = "My laptop won't turn on."
    responses = [
        "Did you try plugging it in? It's not rocket science.",
        "I'm sorry to hear that. Let's start by checking if the power cable is securely connected to both the laptop and the wall outlet."
    ]
    
    for idx, resp in enumerate(responses):
        print(f"\nResponse Option {idx+1}: {resp}")
        score = evaluator.invoke({"user": user_msg, "assistant": resp})
        print(f"Evaluation:\n{score}")

if __name__ == "__main__":
    main()
