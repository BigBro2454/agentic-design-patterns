import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    llm = get_langchain_gemini()
    
    # Researcher Agent
    researcher_prompt = ChatPromptTemplate.from_template(
        "You are a Research Agent. Gather key bullet points about: {topic}. Output ONLY the bullet points."
    )
    researcher = researcher_prompt | llm | StrOutputParser()
    
    # Writer Agent
    writer_prompt = ChatPromptTemplate.from_template(
        "You are a Writer Agent. Turn the following research bullet points into a compelling 2-paragraph blog post.\n"
        "Research:\n{research}"
    )
    writer = writer_prompt | llm | StrOutputParser()
    
    # Editor Agent
    editor_prompt = ChatPromptTemplate.from_template(
        "You are an Editor Agent. Proofread and polish the following draft. Ensure it is punchy and professional.\n"
        "Draft:\n{draft}"
    )
    editor = editor_prompt | llm | StrOutputParser()
    
    topic = "The rise of solid-state batteries in EVs"
    print(f"Workflow Triggered for Topic: '{topic}'\n")
    
    print("Agent 1 (Researcher) is working...")
    research_notes = researcher.invoke({"topic": topic})
    
    print("Agent 2 (Writer) is drafting...")
    draft = writer.invoke({"research": research_notes})
    
    print("Agent 3 (Editor) is polishing...")
    final_post = editor.invoke({"draft": draft})
    
    print(f"\n{'='*40}\nFINAL OUTPUT\n{'='*40}")
    print(final_post)

if __name__ == "__main__":
    main()
