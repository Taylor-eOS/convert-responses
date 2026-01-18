import os
from dataclasses import dataclass
from typing import List
import settings

@dataclass
class Message:
    role: str
    content: str

INPUT_FILE = settings.INPUT_FILE
OUTPUT_FILE = settings.OUTPUT_FILE
#OUTPUT_ROLE = 'Assistant'

while True:
    OUTPUT_ROLE = input("User or Assistant (user/assistant): ").strip().lower()
    if OUTPUT_ROLE in ("u", "user"):
        OUTPUT_ROLE = "User"
        break
    elif OUTPUT_ROLE in ("a", "assistant"):
        OUTPUT_ROLE = "Assistant"
        break
    else:
        print("Invalid input. Please enter 'user' or 'assistant' (or just 'u' or 'a').")

class ConversationParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.messages: List[Message] = []

    def read_file(self) -> str:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"The file {self.filepath} does not exist.")
        with open(self.filepath, 'r', encoding='utf-8') as file:
            return file.read()

    def parse_content(self, content: str):
        blocks = [block.strip() for block in content.split('---')]
        for block in blocks:
            if not block:
                continue
            lines = block.split('\n', 1)
            if len(lines) != 2:
                continue
            role_line, message = lines
            role = role_line.strip().rstrip(':')
            if role not in ['User', 'Assistant']:
                continue
            self.messages.append(Message(role=role, content=message.strip()))

    def get_messages(self) -> List[Message]:
        return self.messages

class MessageWriter:
    def __init__(self, messages: List[Message], output_filepath: str, target_role: str):
        self.messages = messages
        self.output_filepath = output_filepath
        self.target_role = target_role

    def filter_messages(self) -> List[str]:
        return [msg.content for msg in self.messages if msg.role == self.target_role]

    def write_to_file(self, filtered_messages: List[str]):
        with open(self.output_filepath, 'w', encoding='utf-8') as file:
            file.write('\n\n'.join(filtered_messages))
        print(f"Filtered messages have been written to {self.output_filepath}")

def main():
    parser = ConversationParser(INPUT_FILE)
    try:
        content = parser.read_file()
    except FileNotFoundError as e:
        print(e)
        return
    parser.parse_content(content)
    messages = parser.get_messages()
    if not messages:
        print("No valid messages found in the conversation file.")
        return
    writer = MessageWriter(messages, OUTPUT_FILE, OUTPUT_ROLE)
    filtered = writer.filter_messages()
    if not filtered:
        print(f"No messages found for role: {OUTPUT_ROLE}")
        return
    writer.write_to_file(filtered)

if __name__ == "__main__":
    main()

