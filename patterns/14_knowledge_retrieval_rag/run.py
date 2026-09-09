import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def mock_vector_search(query):
    # Mocking a retrieved chunk from a database
    return "Google ADK (Agent Development Kit) allows developers to build robust agents using Python and Gemini."

def main():
    llm = get_langchain_gemini()
    
    rag_prompt = ChatPromptTemplate.from_template(
        "Answer the question based ONLY on the provided context.\n"
        "Context: {context}\n"
        "Question: {question}\n"
        "Answer:"
    )
    rag_chain = rag_prompt | llm | StrOutputParser()
    
    question = "What is Google ADK?"
    print(f"Question: {question}")
    
    print("1. Retrieving context from knowledge base...")
    context = mock_vector_search(question)
    print(f"Context Found: '{context}'")
    
    print("2. Generating answer...")
    answer = rag_chain.invoke({"context": context, "question": question})
    print(f"\nAnswer: {answer}")

if __name__ == "__main__":
    main()
