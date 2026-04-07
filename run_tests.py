import subprocess
import sys
from datetime import datetime
import os

def run_test_case(user_input):
    """Run a single test case using printf to pipe input into agent.py"""
    try:
        # Use printf to send the user input and the 'quit' command to agent.py
        process = subprocess.Popen(
            [sys.executable, "agent.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        stdout, stderr = process.communicate(input=f"{user_input}\nquit\n", timeout=60)
        
        if process.returncode != 0:
            print(f"Error running agent for input: {user_input}")
            print(f"Stderr: {stderr}")
            return False
            
        return True

    except subprocess.TimeoutExpired:
        print(f"Timeout running agent for input: {user_input}")
        return False
    except Exception as e:
        print(f"Exception running agent: {str(e)}")
        return False

def main():
    # Reset test_results.md at the start of the test run
    with open("test_results.md", "w", encoding="utf-8") as f:
        f.write("# KẾT QUẢ TEST CASES CHO TRAVELBUDDY AGENT\n\n")
        f.write(f"**Thời gian chạy:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    test_cases = [
        "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.",
        "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng",
        "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
        "Tôi muốn đặt khách sạn",
        "Giúp tôi giải bài tập lập trình Python về linked list"
    ]

    print("Running 5 test cases...")
    for i, user_input in enumerate(test_cases, 1):
        print(f"Testing {i}/5: {user_input}")
        run_test_case(user_input)
    
    print("\nFinished. Check test_results.md for the logs.")

if __name__ == "__main__":
    main()
