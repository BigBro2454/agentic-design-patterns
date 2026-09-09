import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    sort_prompt = ChatPromptTemplate.from_template(
        "You are an inbox prioritization agent.\n"
        "Rank the following tasks by urgency (High, Medium, Low). Output a sorted list from High to Low.\n"
        "Tasks: {tasks}"
    )
    sorter = sort_prompt | llm | StrOutputParser()
    
    tasks = "- Reply to newsletter subscriber asking about formatting.\n- Server 1 is down and customers cannot check out.\n- Approve PTO request for next month."
    print("Raw Tasks:")
    print(tasks)
    
    print("\nPrioritizing...")
    sorted_tasks = sorter.invoke({"tasks": tasks})
    print(sorted_tasks)

if __name__ == "__main__":
    main()
