import os
import html
from dataclasses import dataclass
from typing import List

@dataclass
class Message:
    role: str  #'User' or 'Assistant'
    content: str

class ConversationParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.messages: List[Message] = []

    #Reads the content of the conversation file.
    def read_file(self) -> str:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"The file {self.filepath} does not exist.")
        with open(self.filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    #Parses the conversation content into messages.
    def parse_content(self, content: str):
        #Split the content by '---' with surrounding blank lines
        blocks = [block.strip() for block in content.split('---')]

        for block in blocks:
            if not block:
                continue  #Skip empty blocks
            lines = block.split('\n', 1)
            if len(lines) != 2:
                print(f"Warning: Unexpected block format:\n{block}\n")
                continue
            role_line, message = lines
            role = role_line.strip().rstrip(':')  #Remove trailing colon
            if role not in ['User', 'Assistant']:
                print(f"Warning: Unknown role '{role}' in block:\n{block}\n")
                continue
            #Normalize line breaks and escape HTML characters
            message = html.escape(message.strip()).replace('\n', '<br>')
            self.messages.append(Message(role=role, content=message))

    #Returns the list of parsed messages.
    def get_messages(self) -> List[Message]:
        return self.messages

class HTMLGenerator:
    def __init__(self, messages: List[Message], output_filepath: str):
        self.messages = messages
        self.output_filepath = output_filepath

    #Generates the HTML content and writes it to the output file.
    def generate_html(self):
        html_content = self.build_html()
        with open(self.output_filepath, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"HTML file has been generated at {self.output_filepath}")

    #Builds the complete HTML structure.
    def build_html(self) -> str:
        #Define the HTML structure with embedded CSS for styling
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
            display: flex;
        }}
        .message.user .avatar {{
            background-color: #007bff;
            color: white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
            font-weight: bold;
        }}
        .message.assistant .avatar {{
            background-color: #28a745;
            color: white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
            font-weight: bold;
        }}
        .message .content {{
            background-color: #f1f1f1;
            padding: 10px 15px;
            border-radius: 8px;
            position: relative;
            max-width: 100%;
        }}
        .message.user .content {{
            background-color: #A9A9A9;
        }}
        .message.assistant .content {{
            background-color: #f1f1f1;
        }}
        .message.user {{
            flex-direction: row;
        }}
        .message.assistant {{
            flex-direction: row-reverse;
        }}
        .message.assistant .content {{
            text-align: left;
        }}
        .message.user .content {{
            text-align: left;
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

    #Builds the HTML for all messages.
    def build_messages(self) -> str:
        message_html = ""
        for msg in self.messages:
            role = msg.role.lower()
            avatar_letter = 'U' if msg.role == 'User' else 'A'
        #    message_block = f"""
        #<div class="message {role}">
        #    <div class="avatar">{avatar_letter}</div>
        #    <div class="content">
        #        <strong>{msg.role}:</strong><br>
        #        {msg.content}
        #    </div>
        #</div>"""
            message_block = f"""
        <div class="message {role}">
            <div class="content">
                <strong>{msg.role}:</strong><br>
                {msg.content}
            </div>
        </div>"""
            message_html += message_block
        return message_html

def main():
    input_filepath = 'conversation.txt'
    output_filepath = 'conversation.html'

    #Parse the conversation file
    parser = ConversationParser(input_filepath)
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

    #Generate the HTML file
    generator = HTMLGenerator(messages, output_filepath)
    generator.generate_html()

if __name__ == "__main__":
    main()

