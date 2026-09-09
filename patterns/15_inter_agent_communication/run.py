import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    agent_a_prompt = ChatPromptTemplate.from_template(
        "You are Agent A (Analyst). The user wants to know about market trends. "
        "Ask Agent B (Data Fetcher) to provide the latest data points."
    )
    agent_a = agent_a_prompt | llm | StrOutputParser()
    
    agent_b_prompt = ChatPromptTemplate.from_template(
        "You are Agent B (Data Fetcher). Agent A asks: '{request}'. "
        "Reply with 3 fake data points about tech stocks."
    )
    agent_b = agent_b_prompt | llm | StrOutputParser()
    
    print("User -> Agent A: 'What are the current market trends?'\n")
    
    request_to_b = agent_a.invoke({})
    print(f"Agent A -> Agent B: {request_to_b}\n")
    
    response_from_b = agent_b.invoke({"request": request_to_b})
    print(f"Agent B -> Agent A: {response_from_b}\n")
    
    print("Agent A processes data and responds to User...")

if __name__ == "__main__":
    main()
