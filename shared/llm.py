import os
from dotenv import load_dotenv
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI

def load_environment():
    """Loads environment variables from .env file."""
    # Try to load from root of agentic-design-patterns
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(env_path)
    
    # Fallback to checking os.environ for either GEMINI_API_KEY or GOOGLE_API_KEY
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY not found in environment variables. Please set it in .env.")
    
    if not os.environ.get("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = api_key
    if not os.environ.get("GOOGLE_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = api_key

def get_gemini_client():
    """Returns a native google.genai client."""
    load_environment()
    return genai.Client()

def get_langchain_gemini(model_name="gemini-2.5-flash", temperature=0, max_retries=3):
    """Returns a LangChain ChatGoogleGenerativeAI instance with retry handling."""
    load_environment()
    return ChatGoogleGenerativeAI(model=model_name, temperature=temperature, max_retries=max_retries)
