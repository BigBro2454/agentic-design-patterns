"""
Deterministic Headless Mock LLM for CI and local evaluation.
Allows testing all 21 Agentic Design Patterns without external API keys or token burn.
"""
import json
import re
from typing import Any, Dict, List, Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, ToolCall
from langchain_core.outputs import ChatGeneration, ChatResult


class MockChatModel(BaseChatModel):
    """Deterministic, headless ChatModel designed for multi-agent pattern testing."""

    model_name: str = "mock-gemini-2.5-flash"
    bound_tools: list = []

    @property
    def _llm_type(self) -> str:
        return "mock-chat-model"

    def bind_tools(self, tools: Any, **kwargs: Any) -> Any:
        """Emulate tool binding required by LangGraph and ReAct agents."""
        return self.model_copy(update={"bound_tools": list(tools)})

    def _generate_response_content(self, prompt_text: str, messages: List[BaseMessage]) -> tuple[str, list[ToolCall]]:
        """Intelligently match patterns based on prompt text and conversation context."""
        lower_prompt = prompt_text.lower()

        # Handle bound tools invocation (Pattern 05: Tool Use)
        if self.bound_tools:
            has_tool_response = any(getattr(m, "type", "") == "tool" for m in messages)
            if not has_tool_response:
                # Return tool call for first tool
                tool_name = getattr(self.bound_tools[0], "name", "get_weather")
                return "", [ToolCall(name=tool_name, args={"location": "Tokyo"}, id="call_mock_weather_1")]
            else:
                return (
                    "The current weather in Tokyo is 22°C and sunny. "
                    "You do not need to pack an umbrella, as clear skies are expected.",
                    []
                )

        # Pattern 01: Prompt Chaining
        if "extract the technical specifications" in lower_prompt:
            return "cpu: 3.5 GHz octa-core\nmemory: 16GB\nstorage: 1TB NVMe SSD", []
        if "transform the following specifications into a json object" in lower_prompt:
            return json.dumps({
                "cpu": "3.5 GHz octa-core",
                "memory": "16GB",
                "storage": "1TB NVMe SSD"
            }, indent=2), []

        # Pattern 02: Routing
        if "classify it into exactly one of these categories" in lower_prompt:
            if "router" in lower_prompt or "internet" in lower_prompt or "connection" in lower_prompt:
                return "tech_support", []
            elif "charged" in lower_prompt or "subscription" in lower_prompt or "billing" in lower_prompt:
                return "billing", []
            return "general", []
        if "you are a technical support agent" in lower_prompt:
            return "Please power-cycle your router by unplugging it for 30 seconds and check line connectivity.", []
        if "you are a billing specialist" in lower_prompt:
            return "We have reviewed your invoice and refunded the duplicate charge of $29.99 to your original payment method.", []
        if "you are a helpful assistant. respond to:" in lower_prompt:
            return "Hello! How can I assist you with your account today?", []

        # Pattern 03: Parallelization
        if "write a short paragraph about the" in lower_prompt:
            return f"Synthesized overview addressing key strategic considerations for this domain.", []

        # Pattern 04: Reflection
        if "review the following marketing pitch" in lower_prompt and "approved" in lower_prompt:
            return "APPROVED", []
        if "write a 2-sentence marketing pitch for a new smart coffee mug" in lower_prompt:
            return (
                "Meet the SmartMug with precision temperature control that keeps your brew at the ideal temperature all day. "
                "Enjoy barista-level perfection wherever work takes you."
            ), []

        # Pattern 06: Planning
        if "break down the following objective into a 3-step actionable plan" in lower_prompt:
            return (
                "1. Define audience persona and select email newsletter software.\n"
                "2. Curate initial technical topics and design newsletter template.\n"
                "3. Broadcast inaugural issue and monitor reader engagement metrics."
            ), []
        if "execute the following step of a plan" in lower_prompt:
            return "Plan step executed successfully with verified milestone output.", []

        # Pattern 07: Multi-Agent Orchestration
        if "you are a research agent" in lower_prompt:
            return (
                "- Solid-state batteries deliver up to 2x higher volumetric energy density than traditional Li-ion cells.\n"
                "- Non-flammable ceramic/polymer electrolytes dramatically lower thermal runaway risk.\n"
                "- Major automotive OEMs target commercial series production between 2027 and 2028."
            ), []
        if "you are a writer agent" in lower_prompt:
            return (
                "Solid-state battery technology is rapidly revolutionizing electric mobility. By replacing flammable liquid "
                "electrolytes with resilient solid counterparts, these next-generation cells eliminate thermal runaway while "
                "substantially expanding driving range.\n\n"
                "Automotive manufacturers worldwide are progressing toward commercial-scale manufacturing. With target timelines "
                "converging around 2028, drivers can anticipate 500-mile journeys and ten-minute charging stops."
            ), []
        if "you are an editor agent" in lower_prompt:
            return (
                "The electric vehicle transition is approaching an inflection point with solid-state batteries. Doubling energy "
                "density while virtually eliminating fire risks, solid-state architecture sets a new standard for performance.\n\n"
                "With tier-one manufacturers accelerating pilot production for 2028, ultra-fast charging and 500-mile ranges will soon "
                "transition from laboratory benchmarks to highway reality."
            ), []

        # Pattern 08: Memory Management
        if "extract any durable user preferences" in lower_prompt:
            if "antonio" in lower_prompt:
                return "name: Antonio\npreferred_language: Python", []
            return "NONE", []
        if "you are a helpful assistant with persistent memory" in lower_prompt:
            return "Your name is Antonio, and your preferred programming language is Python!", []

        # Pattern 09: Learning and Adaptation
        if "explain how a neural network works" in lower_prompt:
            if "5 years old" in lower_prompt or "food" in lower_prompt:
                return (
                    "Imagine a neural network is like a team of bakers making cookies! The first baker checks the flour, "
                    "the second tastes the sugar, and the head chef decides if the cookie is yummy. They practice until "
                    "every batch is baked to perfection!"
                ), []
            return (
                "A neural network is a machine learning architecture inspired by biological neurons. It processes features "
                "through interconnected layers of mathematical nodes, optimizing internal weights using gradient descent and "
                "backpropagation."
            ), []

        # Pattern 10: Model Context Protocol (MCP)
        if "you are an equity research assistant" in lower_prompt:
            return (
                "Based on MCP market intelligence, Alphabet Inc. (GOOGL) trades at $182.40 USD (+1.85%). "
                "With an EPS of $6.50, its current price-to-earnings (P/E) multiple stands at 28.06x, positioned attractively "
                "against the peer benchmark multiple of 28.5x."
            ), []

        # Pattern 11: Goal Setting and Monitoring
        if "calculate a progress percentage" in lower_prompt:
            if "blank document" in lower_prompt:
                return "Progress: 10% | Next: Outline plot chapters", []
            elif "chapter 1" in lower_prompt:
                return "Progress: 50% | Next: Draft final chapter", []
            return "Progress: 100% | Next: Publish completed manuscript", []

        # Pattern 12: Exception Handling and Recovery
        if "suggest an immediate fallback or recovery action" in lower_prompt:
            return "Fallback Strategy: Trip circuit breaker, switch to standby database replica, and notify site reliability team.", []

        # Pattern 13: Human in the Loop
        if "generate a bash command to delete all log files" in lower_prompt:
            return "find /var/logs -type f -mtime +30 -name '*.log' -delete", []

        # Pattern 14: Knowledge Retrieval (RAG)
        if "answer the question based only on the provided context" in lower_prompt:
            return "Google ADK (Agent Development Kit) allows developers to build robust agents using Python and Gemini.", []

        # Pattern 15: Inter-Agent Communication
        if "you are agent a (analyst)" in lower_prompt:
            return "Please retrieve the latest quarterly performance telemetry for leading tech equities.", []
        if "you are agent b (data fetcher)" in lower_prompt:
            return "1. Alphabet: +14% Cloud YoY\n2. Apple: $94B services run-rate\n3. Microsoft: Azure +29% YoY", []

        # Pattern 16: Resource Aware Optimization
        if "is this query 'simple' or 'complex'?" in lower_prompt:
            if "2+2" in lower_prompt:
                return "simple", []
            return "complex", []

        # Pattern 17: Reasoning Techniques (Chain of Thought)
        if "let's think step by step before giving the final answer" in lower_prompt:
            return (
                "Step 1: Fill the 5-liter jug completely (5L).\n"
                "Step 2: Pour water from the 5L jug into the 3L jug until full. The 5L jug now contains 2L.\n"
                "Step 3: Empty the 3L jug.\n"
                "Step 4: Pour the remaining 2L from the 5L jug into the 3L jug.\n"
                "Step 5: Fill the 5L jug completely (5L).\n"
                "Step 6: Carefully pour from the 5L jug into the 3L jug until the 3L jug is full (needs 1L).\n"
                "Step 7: Exactly 4 liters remain in the 5-liter jug."
            ), []

        # Pattern 18: Guardrails and Safety
        if "if it asks for illegal acts, violence, or hacking" in lower_prompt:
            input_section = lower_prompt.split("input:")[-1] if "input:" in lower_prompt else lower_prompt
            if any(bad_word in input_section for bad_word in ("bypass", "firewall", "exploit", "ddos", "hack")):
                return "BLOCK", []
            return "PASS", []

        # Pattern 19: Evaluation and Monitoring
        if "evaluate the assistant's response on a scale of 1 to 5" in lower_prompt:
            if "rocket science" in lower_prompt:
                return "Helpfulness: 2, Tone: 1, Notes: Unprofessional condescension detected.", []
            return "Helpfulness: 5, Tone: 5, Notes: Exemplary empathy and methodical troubleshooting steps.", []

        # Pattern 20: Prioritization
        if "rank the following tasks by urgency" in lower_prompt:
            return (
                "1. High: Server 1 is down and customers cannot check out.\n"
                "2. Medium: Reply to newsletter subscriber asking about formatting.\n"
                "3. Low: Approve PTO request for next month."
            ), []

        # Pattern 21: Exploration and Discovery
        if "generate 2 interesting hypotheses to explore" in lower_prompt:
            return (
                "1. Ambient temperatures above 28°C correlate with a 38% increase in dairy-free sorbet preference.\n"
                "2. Promotional bundles pairing artisan toppings with fruit bases yield 22% higher basket conversion on weekends."
            ), []

        # Fallback default
        return "Deterministic mock response executed successfully for agent pattern.", []

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        full_text = " ".join(str(m.content) for m in messages)
        content, tool_calls = self._generate_response_content(full_text, messages)
        message = AIMessage(content=content, tool_calls=tool_calls)
        return ChatResult(generations=[ChatGeneration(message=message)])

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        return self._generate(messages, stop, run_manager, **kwargs)
