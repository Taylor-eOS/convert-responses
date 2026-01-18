import os
import html
from dataclasses import dataclass
from typing import List
from weasyprint import HTML
import settings

@dataclass
class Message:
    role: str
    content: str

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
            message = html.escape(message.strip()).replace('\n', '<br>')
            self.messages.append(Message(role=role, content=message))

    def get_messages(self) -> List[Message]:
        return self.messages

class PDFGenerator:
    def __init__(self, messages: List[Message], output_filepath: str):
        self.messages = messages
        self.output_filepath = output_filepath

    def generate_pdf(self):
        html_content = self.build_html()
        HTML(string=html_content).write_pdf(self.output_filepath)
        print(f"PDF file has been generated at {self.output_filepath}")

    def build_html(self) -> str:
        html_structure = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Conversation</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        .message {{
            margin-bottom: 20px;
        }}
        .message.user .content {{
            background-color: #D3D3D3;
            padding: 10px 15px;
            border-radius: 8px;
            text-align: left;
        }}
        .message.assistant .content {{
            background-color: #A9A9A9;
            padding: 10px 15px;
            border-radius: 8px;
            text-align: left;
        }}
        .role {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        {self.build_messages()}
    </div>
</body>
</html>
"""
        return html_structure

    def build_messages(self) -> str:
        message_html = ""
        for msg in self.messages:
            role = msg.role.lower()
            message_block = f"""
        <div class="message {role}">
            <div class="role">{msg.role}:</div>
            <div class="content">
                {msg.content}
            </div>
        </div>
"""
            message_html += message_block
        return message_html

def main():
    INPUT_FILE = settings.INPUT_FILE
    OUTPUT_FILE = OUTPUT_FILE = os.path.splitext(INPUT_FILE)[0] + '.pdf'
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
    generator = PDFGenerator(messages, OUTPUT_FILE)
    generator.generate_pdf()

if __name__ == "__main__":
    main()

