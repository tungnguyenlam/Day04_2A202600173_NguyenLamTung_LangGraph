import json
import os
from datetime import datetime

class ConversationLogger:
    def __init__(self, log_file="test_results.md"):
        self.log_file = log_file
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("# KẾT QUẢ TEST CASES CHO TRAVELBUDDY AGENT\n\n")

    def log_interaction(self, user_input, agent_response, tool_calls=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"### Interaction at {timestamp}\n\n")
            f.write(f"**User:**\n> {user_input}\n\n")
            
            if tool_calls:
                f.write("**Tool Calls:**\n")
                for tc in tool_calls:
                    f.write(f"- `{tc['name']}({json.dumps(tc['args'], ensure_ascii=False)})`\n")
                f.write("\n")
            
            f.write(f"**TravelBuddy:**\n{agent_response}\n\n")
            f.write("---\n\n")

logger = ConversationLogger()
