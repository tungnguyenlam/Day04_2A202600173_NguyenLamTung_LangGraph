from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.language_models import BaseLanguageModel
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import List, Optional
from tools import search_flights, search_hotels, calculate_budget
from logger import logger
from dotenv import load_dotenv
import os
import json

load_dotenv()


# Mock LLM for testing when no API key is available
class MockLLM(BaseLanguageModel):
    """A mock LLM that simulates responses for testing the TravelBuddy agent"""

    def _generate(
        self,
        messages,
        stop=None,
        run_manager=None,
        **kwargs,
    ):
        # Get the last human message
        last_message = messages[-1]
        if hasattr(last_message, "content"):
            user_input = last_message.content
        else:
            user_input = str(last_message)

        # Simulate LLM responses based on user input
        user_input_lower = user_input.lower()

        # Test 1: Greeting - should respond directly without tools
        if any(
            greeting in user_input_lower for greeting in ["xin chào", "hello", "hi"]
        ) and any(word in user_input_lower for word in ["du lịch", "travel", "đi đâu"]):
            response_text = "Xin chào! Rất vui được giúp bạn lên kế hoạch chuyến đi. Bạn có thể cho tôi biết bạn muốn đi đâu, khi nào, và có ngân sách khoảng bao nhiêu không?"
            message = AIMessage(content=response_text)
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])

        # Test 2: Flight search request
        elif "chuyến bay" in user_input_lower and (
            "hà nội" in user_input_lower and "đà nẵng" in user_input_lower
        ):
            # Return a tool call for search_flights
            message = AIMessage(
                content="",
                tool_calls=[
                    {
                        "id": "call_1",
                        "name": "search_flights",
                        "args": {"origin": "Hà Nội", "destination": "Đà Nẵng"},
                    }
                ],
            )
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])

        # Test 3: Multi-step request (flight + hotel + budget)
        elif (
            "phú quốc" in user_input_lower
            and ("2 đêm" in user_input_lower or "2 night" in user_input_lower)
            and "5 triệu" in user_input_lower
        ):
            # First, return a tool call for search_flights
            message = AIMessage(
                content="",
                tool_calls=[
                    {
                        "id": "call_1",
                        "name": "search_flights",
                        "args": {"origin": "Hà Nội", "destination": "Phú Quốc"},
                    }
                ],
            )
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])

        # Test 4: Hotel request missing info
        elif "đặt khách sạn" in user_input_lower and len(user_input_lower.split()) < 5:
            response_text = "Bạn muốn đặt khách sạn ở thành phố nào? Bạn có bao nhiêu đêm và ngân sách cho mỗi đêm là bao nhiêu?"
            message = AIMessage(content=response_text)
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])

        # Test 5: Off-topic request
        elif (
            "bài tập" in user_input_lower
            or "lập trình" in user_input_lower
            or "linked list" in user_input_lower
        ):
            response_text = "Xin lỗi, tôi chỉ có thể giúp bạn về các vấn đề liên quan đến du lịch như tìm vé máy bay, khách sạn, và tính ngân sách. Bạn có thể hỏi tôi về chuyến đi của mình không?"
            message = AIMessage(content=response_text)
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])

        # Default response
        else:
            response_text = "Cảm ơn bạn đã hỏi! Tôi là TravelBuddy, trợ lý du lịch của bạn. Bạn có thể giúp tôi biết bạn muốn đi đâu, khi nào, và có ngân sách bao nhiêu để tôi có thể tìm kiếm những lựa chọn phù hợp nhất cho bạn?"
            message = AIMessage(content=response_text)
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])

    def _llm_type(self):
        return "mock"

    def bind_tools(self, tools):
        # Return self for simplicity in mock
        return self


# Provider loader
def load_llm():
    """Load LLM based on DEFAULT_PROVIDER in .env"""
    provider = os.getenv("DEFAULT_PROVIDER", "openrouter").lower()

    # Check if we have valid API keys
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    has_valid_key = (
        provider == "openrouter"
        and openrouter_key
        and not openrouter_key.startswith("sk-or-test")
    ) or (provider == "openai" and openai_key and not openai_key.startswith("sk-test"))

    if not has_valid_key:
        print("Warning: No valid API key found. Using MockLLM for testing.")
        return MockLLM()

    if provider == "openai":
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        api_key = os.getenv("OPENAI_API_KEY")
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model, api_key=api_key)

    elif provider == "openrouter":
        model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        api_key = os.getenv("OPENROUTER_API_KEY")
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=model, api_key=api_key, base_url="https://openrouter.ai/api/v1"
        )

    elif provider == "gemini":
        print(
            "Warning: Gemini provider selected but langchain-google-genai not installed. Falling back to MockLLM."
        )
        return MockLLM()

    elif provider == "ollama":
        print(
            "Warning: Ollama provider selected but langchain-ollama not installed. Falling back to MockLLM."
        )
        return MockLLM()

    else:
        print(f"Warning: Unknown provider '{provider}'. Falling back to MockLLM.")
        return MockLLM()


# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = load_llm()
llm_with_tools = llm.bind_tools(tools_list)


# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    # === LOGGING ===
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tc in response.tool_calls:
            print(f"Gọi tool: {tc['name']}({tc['args']})")
    else:
        print(f"Trả lời trực tiếp")

    return {"messages": [response]}


# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Define edges
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy — Trợ lý Du lịch Thông minh")
    print("Gõ 'quit' để thoát")
    print("=" * 60)

    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\nTravelBuddy đang suy nghĩ...")
        result = graph.invoke({"messages": [("human", user_input)]})
        
        # Collect tool calls from intermediate messages
        tool_calls = []
        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    tool_calls.append({"name": tc["name"], "args": tc["args"]})

        final_response = result["messages"][-1].content
        print(f"\nTravelBuddy: {final_response}")
        
        # Log the interaction
        logger.log_interaction(user_input, final_response, tool_calls if tool_calls else None)
