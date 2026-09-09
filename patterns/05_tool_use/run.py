import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def get_weather(location: str) -> str:
    """Get the current weather in a given location."""
    # Mock implementation
    weather_data = {
        "london": "15°C and rainy",
        "tokyo": "22°C and sunny",
        "new york": "18°C and cloudy"
    }
    return weather_data.get(location.lower(), "Unknown location. Please try London, Tokyo, or New York.")

def main():
    llm = get_langchain_gemini()
    tools = [get_weather]
    
    agent = create_react_agent(llm, tools)
    
    query = "What is the weather like in Tokyo right now? Should I pack an umbrella?"
    print(f"Query: {query}\n")
    print("Executing Tool Calling Agent (LangGraph ReAct)...")
    
    result = agent.invoke({"messages": [("user", query)]})
    final_message = result["messages"][-1]
    print("\nFinal Output:\n", final_message.content)

if __name__ == "__main__":
    main()
