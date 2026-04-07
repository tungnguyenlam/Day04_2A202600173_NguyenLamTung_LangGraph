#!/usr/bin/env python3
"""
Debug script to test the agent step by step
"""

from agent import graph


def test_simple():
    print("Testing simple greeting...")
    result = graph.invoke({"messages": [("human", "Xin chào!")]})
    print("Result:", result)
    print("Last message:", result["messages"][-1])


if __name__ == "__main__":
    test_simple()
