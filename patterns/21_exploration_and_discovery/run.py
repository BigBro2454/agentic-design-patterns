import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    hypothesis_prompt = ChatPromptTemplate.from_template(
        "You are an AI research agent exploring a dataset. The dataset contains sales numbers for an ice cream shop over a year.\n"
        "Generate 2 interesting hypotheses to explore regarding seasonality and flavor trends."
    )
    explorer = hypothesis_prompt | llm | StrOutputParser()
    
    print("Agent is exploring the environment (Dataset: Ice Cream Sales)...")
    hypotheses = explorer.invoke({})
    
    print(f"\nGenerated Hypotheses for Discovery:\n{hypotheses}")

if __name__ == "__main__":
    main()
