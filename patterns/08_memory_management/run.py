import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

class AgentMemoryManager:
    """Production Multi-Tiered Memory Manager:
    - Tier 1: Working Session Buffer (short-term conversation history)
    - Tier 2: Semantic Long-Term Entity Store (persisted user facts & preferences)
    """
    def __init__(self, llm):
        self.llm = llm
        self.chat_history = []
        self.long_term_facts = {}

    def extract_and_store_facts(self, user_input: str):
        """Extracts durable facts/preferences from user input into long-term memory."""
        fact_prompt = ChatPromptTemplate.from_template(
            "Extract any durable user preferences, facts, or attributes from this input as key: value pairs.\n"
            "If none, output NONE.\n"
            "Input: {input}\n"
            "Facts:"
        )
        extractor = fact_prompt | self.llm | StrOutputParser()
        result = extractor.invoke({"input": user_input}).strip()
        if result and "NONE" not in result.upper():
            for line in result.split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    self.long_term_facts[k.strip().lower()] = v.strip()

    def get_system_prompt_with_memory(self) -> str:
        facts_summary = "\n".join([f"- {k}: {v}" for k, v in self.long_term_facts.items()]) if self.long_term_facts else "None"
        return (
            "You are a helpful assistant with persistent memory.\n"
            f"Known facts about the user:\n{facts_summary}\n"
            "Use these facts to personalize your responses."
        )

    def chat(self, user_input: str) -> str:
        # 1. Update long-term memory
        self.extract_and_store_facts(user_input)
        
        # 2. Assemble prompt with system memory + working buffer
        system_msg = SystemMessage(content=self.get_system_prompt_with_memory())
        messages = [system_msg] + self.chat_history + [HumanMessage(content=user_input)]
        
        # 3. Call LLM
        response = self.llm.invoke(messages)
        
        # 4. Append to short-term buffer
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=response.content))
        
        return response.content

def main():
    llm = get_langchain_gemini()
    memory_manager = AgentMemoryManager(llm)
    
    dialogue = [
        "Hi, I'm Antonio and my favorite programming language is Python.",
        "Can you remind me what my name is and what programming language I prefer?"
    ]
    
    print("=== Pattern 08: Multi-Tiered Memory Management ===")
    for query in dialogue:
        print(f"\nUser: {query}")
        reply = memory_manager.chat(query)
        print(f"Agent: {reply}")
        print(f"[Current Long-Term Fact Store]: {memory_manager.long_term_facts}")

if __name__ == "__main__":
    main()

