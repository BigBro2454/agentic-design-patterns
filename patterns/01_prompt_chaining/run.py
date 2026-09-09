import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    prompt_extract = ChatPromptTemplate.from_template("Extract the technical specifications from the following text:\n\n{text_input}")
    prompt_transform = ChatPromptTemplate.from_template("Transform the following specifications into a JSON object with 'cpu', 'memory', and 'storage' as keys:\n\n{specifications}")
    
    extraction_chain = prompt_extract | llm | StrOutputParser()
    full_chain = {"specifications": extraction_chain} | prompt_transform | llm | StrOutputParser()
    
    input_text = "The new laptop model features a 3.5 GHz octa-core processor, 16GB of RAM, and a 1TB NVMe SSD."
    print("Input:", input_text)
    print("Running Prompt Chain...")
    
    result = full_chain.invoke({"text_input": input_text})
    print("\n--- Final JSON Output ---")
    print(result)

if __name__ == "__main__":
    main()
