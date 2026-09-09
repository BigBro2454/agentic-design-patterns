import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    action_prompt = ChatPromptTemplate.from_template(
        "Generate a bash command to delete all log files older than 30 days in /var/logs.\n"
        "Output ONLY the command."
    )
    action_chain = action_prompt | llm | StrOutputParser()
    
    print("Agent is preparing a high-risk action...")
    command = action_chain.invoke({}).strip()
    
    print(f"\n⚠️  WARNING: Agent wants to execute the following command:")
    print(f"> {command}\n")
    
    # In a real environment, you would use input() here. 
    # For automated execution, we will mock the user's rejection.
    user_input = "no" # Mocking: input("Approve execution? (yes/no): ")
    print(f"User Input: {user_input}")
    
    if user_input.lower() in ['yes', 'y']:
        print("Executing command...")
    else:
        print("Execution aborted by Human-in-the-Loop constraint.")

if __name__ == "__main__":
    main()
