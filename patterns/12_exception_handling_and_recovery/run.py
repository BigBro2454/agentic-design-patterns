import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def flacky_api_call():
    """Mock API that fails 70% of the time."""
    if random.random() < 0.7:
        raise ValueError("API Connection Timeout")
    return "Data retrieved successfully: [User ID 1042]"

def main():
    llm = get_langchain_gemini()
    
    recovery_prompt = ChatPromptTemplate.from_template(
        "An operation failed with error: {error}. Suggest an immediate fallback or recovery action for the user."
    )
    recovery_chain = recovery_prompt | llm | StrOutputParser()
    
    print("Attempting to call flaky API...")
    max_retries = 3
    success = False
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}...")
            result = flacky_api_call()
            print(f"✅ Success: {result}")
            success = True
            break
        except Exception as e:
            print(f"❌ Error caught: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
            else:
                print("Max retries reached. Triggering LLM Recovery Strategy...")
                recovery_plan = recovery_chain.invoke({"error": str(e)})
                print(f"\nAgent Recovery Plan:\n{recovery_plan}")

if __name__ == "__main__":
    main()
