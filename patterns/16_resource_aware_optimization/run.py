import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    # In a real system, you might route to "gemini-2.5-flash" for simple tasks
    # and "gemini-1.5-pro" for complex reasoning to save tokens and latency.
    flash_llm = get_langchain_gemini(model_name="gemini-2.5-flash")
    
    router_prompt = ChatPromptTemplate.from_template(
        "Is this query 'simple' or 'complex'?\nQuery: {query}\nOutput only 'simple' or 'complex'."
    )
    router = router_prompt | flash_llm | StrOutputParser()
    
    queries = ["What is 2+2?", "Can you write a python script to solve the traveling salesperson problem using genetic algorithms?"]
    
    for q in queries:
        complexity = router.invoke({"query": q}).strip().lower()
        print(f"Query: '{q}' -> Classified as: {complexity}")
        if "simple" in complexity:
            print("Routing to fast/cheap model (Flash).")
        else:
            print("Routing to capable/expensive model (Pro).")
        print("-" * 20)

if __name__ == "__main__":
    main()
