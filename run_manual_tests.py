#!/usr/bin/env python3
"""
Manual test script for TravelBuddy agent
Runs the 5 test cases from the assignment and captures outputs
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import graph
from langchain_core.messages import HumanMessage, SystemMessage


def run_test_case(test_name, user_input):
    """Run a single test case and return the output"""
    print(f"\n{'=' * 60}")
    print(f"Running {test_name}")
    print(f"User input: {user_input}")
    print("=" * 60)

    try:
        # Run the agent with the input
        result = graph.invoke({"messages": [HumanMessage(content=user_input)]})

        # Extract the agent's response
        agent_response = result["messages"][-1].content
        print(f"Agent response:\n{agent_response}")
        return agent_response

    except Exception as e:
        error_msg = f"Error running test: {str(e)}"
        print(f"ERROR: {error_msg}")
        return error_msg


def main():
    print("TravelBuddy Agent Test Suite")
    print("============================")

    test_cases = [
        (
            "Test 1 — Direct Answer (Không cần tool)",
            "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.",
        ),
        ("Test 2 — Single Tool Call", "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"),
        (
            "Test 3 — Multi-Step Tool Chaining",
            "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
        ),
        ("Test 4 — Missing Info / Clarification", "Tôi muốn đặt khách sạn"),
        (
            "Test 5 — Guardrail / Refusal",
            "Giúp tôi giải bài tập lập trình Python về linked list",
        ),
    ]

    results = []

    for test_name, user_input in test_cases:
        response = run_test_case(test_name, user_input)
        results.append(
            {
                "test_name": test_name,
                "user_input": user_input,
                "agent_response": response,
            }
        )

    # Write results to test_results.md
    with open("test_results.md", "w", encoding="utf-8") as f:
        f.write("# KẾT QUẢ TEST CASES CHO TRAVELBUDDY AGENT\n\n")
        from datetime import datetime

        f.write(
            f"**Thời gian chạy:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )

        for i, result in enumerate(results, 1):
            f.write(f"## {result['test_name']}\n\n")
            f.write(f"**User:**\n\n> {result['user_input']}\n\n")
            f.write(f"**TravelBuddy:**\n\n{result['agent_response']}\n\n")
            f.write("---\n\n")

    print(f"\n{'=' * 60}")
    print("Test results saved to test_results.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
