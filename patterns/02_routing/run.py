import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    # 1. Router prompt
    router_prompt = ChatPromptTemplate.from_template(
        "Analyze the following user query and classify it into exactly one of these categories: 'tech_support', 'billing', or 'general'.\n"
        "Output ONLY the category name.\n\nQuery: {query}"
    )
    router_chain = router_prompt | llm | StrOutputParser()
    
    # 2. Handlers
    def tech_support_handler(query):
        prompt = ChatPromptTemplate.from_template("You are a technical support agent. Help with this issue:\n{query}")
        return (prompt | llm | StrOutputParser()).invoke({"query": query})
        
    def billing_handler(query):
        prompt = ChatPromptTemplate.from_template("You are a billing specialist. Help with this payment issue:\n{query}")
        return (prompt | llm | StrOutputParser()).invoke({"query": query})
        
    def general_handler(query):
        prompt = ChatPromptTemplate.from_template("You are a helpful assistant. Respond to:\n{query}")
        return (prompt | llm | StrOutputParser()).invoke({"query": query})

    # 3. Execution
    queries = [
        "My internet router keeps dropping the connection.",
        "I was charged twice for my subscription this month."
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        category = router_chain.invoke({"query": query}).strip().lower()
        print(f"Routed to: {category}")
        
        if 'tech_support' in category:
            response = tech_support_handler(query)
        elif 'billing' in category:
            response = billing_handler(query)
        else:
            response = general_handler(query)
            
        print(f"Response: {response}\n{'-'*40}")

if __name__ == "__main__":
    main()
