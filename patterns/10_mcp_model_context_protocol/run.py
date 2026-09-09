import sys
import os
import asyncio
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm import get_langchain_gemini
from mcp.server.mcpserver import MCPServer
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Initialize MCP Server
mcp_server = MCPServer("financial-intelligence-mcp")

@mcp_server.tool()
def get_stock_quote(ticker: str) -> str:
    """Fetch the real-time stock price and trading volume for a ticker symbol."""
    mock_quotes = {
        "GOOGL": {"price": 182.40, "currency": "USD", "change": "+1.85%"},
        "AAPL": {"price": 224.10, "currency": "USD", "change": "-0.40%"},
        "MSFT": {"price": 448.20, "currency": "USD", "change": "+0.92%"}
    }
    data = mock_quotes.get(ticker.upper(), {"error": f"Ticker {ticker} not found."})
    return json.dumps(data)

@mcp_server.tool()
def compute_valuation_metrics(ticker: str, price: float, eps: float) -> str:
    """Compute financial valuation multiples including P/E ratio."""
    pe_ratio = round(price / eps, 2) if eps > 0 else "N/A"
    return json.dumps({"ticker": ticker.upper(), "pe_ratio": pe_ratio, "benchmark_pe": 28.5})

async def run_mcp_agent():
    print("=== Pattern 10: Model Context Protocol (MCP) Runtime ===\n")
    
    # 2. Inspect tools exposed via MCP Protocol
    tools = await mcp_server.list_tools()
    print(f"📡 MCP Server '{mcp_server.name}' discovered {len(tools)} tools:")
    for t in tools:
        print(f"  - Tool: {t.name} -> {t.description}")
        
    llm = get_langchain_gemini()
    
    # 3. Agent planning with MCP Tools
    user_query = "What is the current stock quote for GOOGL, and what is its P/E ratio if EPS is $6.50?"
    print(f"\nUser Query: {user_query}\n")
    
    # Step A: Agent calls MCP get_stock_quote tool
    print("🤖 Agent calling MCP Tool: 'get_stock_quote(ticker=\"GOOGL\")'...")
    quote_res = await mcp_server.call_tool("get_stock_quote", {"ticker": "GOOGL"})
    quote_data = json.loads(quote_res.content[0].text)
    print(f"📥 MCP Tool Response: {quote_data}")
    
    price = quote_data["price"]
    
    # Step B: Agent calls MCP compute_valuation_metrics tool
    print(f"\n🤖 Agent calling MCP Tool: 'compute_valuation_metrics(ticker=\"GOOGL\", price={price}, eps=6.50)'...")
    metrics_res = await mcp_server.call_tool("compute_valuation_metrics", {"ticker": "GOOGL", "price": price, "eps": 6.50})
    metrics_data = json.loads(metrics_res.content[0].text)
    print(f"📥 MCP Tool Response: {metrics_data}")
    
    # Step C: Synthesize final response using LLM
    synthesis_prompt = ChatPromptTemplate.from_template(
        "You are an equity research assistant. Synthesize a professional response to the user's query.\n"
        "User Query: {query}\n"
        "MCP Data Retrieved: Stock Quote: {quote}, Valuation Metrics: {metrics}\n"
        "Response:"
    )
    chain = synthesis_prompt | llm | StrOutputParser()
    final_output = chain.invoke({"query": user_query, "quote": quote_data, "metrics": metrics_data})
    
    print("\n" + "=" * 50)
    print("FINAL AGENT RESPONSE (Powered by MCP Context)")
    print("=" * 50)
    print(final_output)

def main():
    asyncio.run(run_mcp_agent())

if __name__ == "__main__":
    main()

