import sys
import os
import concurrent.futures
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_section(topic, section_name):
    llm = get_langchain_gemini()
    prompt = ChatPromptTemplate.from_template("Write a short paragraph about the {section_name} of {topic}.")
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"topic": topic, "section_name": section_name})

def main():
    topic = "Artificial Intelligence"
    sections = ["History", "Current Applications", "Future Ethics"]
    print(f"Generating report for: {topic} (in parallel)\n")
    
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_section = {executor.submit(generate_section, topic, sec): sec for sec in sections}
        for future in concurrent.futures.as_completed(future_to_section):
            sec = future_to_section[future]
            try:
                results[sec] = future.result()
                print(f"✅ Completed section: {sec}")
            except Exception as exc:
                print(f"❌ Section {sec} generated an exception: {exc}")
                
    print("\n--- Final Compiled Report ---")
    for sec in sections:
        print(f"\n### {sec}\n{results.get(sec, 'Failed')}")

if __name__ == "__main__":
    main()
