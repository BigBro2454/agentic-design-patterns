import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    # The agent dynamically adapts to the "learned" style injected into the prompt
    adaptive_prompt = ChatPromptTemplate.from_template(
        "You are an assistant. Answer the user's question.\n"
        "Apply the following style/preference if provided: {learned_preference}\n\n"
        "Question: {question}"
    )
    chain = adaptive_prompt | llm | StrOutputParser()
    
    question = "Explain how a neural network works."
    
    print("--- Before Adaptation ---")
    response_1 = chain.invoke({"learned_preference": "None", "question": question})
    print(response_1[:300] + "...\n")
    
    print("--- After Adaptation (Learned: User prefers ELI5 analogies) ---")
    learned_rule = "Explain it like I am 5 years old using food analogies."
    response_2 = chain.invoke({"learned_preference": learned_rule, "question": question})
    print(response_2[:300] + "...\n")

if __name__ == "__main__":
    main()
