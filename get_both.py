import os
import sys
from dataclasses import dataclass
from typing import List
try:
    import pysbd
except Exception:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pysbd"])
    import pysbd

INPUT_FILE = 'conversation.txt'
OUTPUT_FILE = 'filtered_conversation.txt'

@dataclass
class Message:
    role: str
    content: str

def read_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_messages(content: str) -> List[Message]:
    blocks = [b.strip() for b in content.split('---')]
    msgs: List[Message] = []
    for block in blocks:
        if not block:
            continue
        first_line_break = block.find('\n')
        if first_line_break == -1:
            continue
        role_line = block[:first_line_break].strip().rstrip(':')
        body = block[first_line_break+1:].strip()
        rl = role_line.lower()
        if rl.startswith('user'):
            msgs.append(Message(role='User', content=body))
        elif rl.startswith('assistant'):
            msgs.append(Message(role='Assistant', content=body))
    return msgs

def summarize_assistant(text: str, max_sentences: int = 3, lang: str = 'en') -> str:
    if not text.strip():
        return ''
    seg = pysbd.Segmenter(language=lang, clean=False)
    try:
        sents = seg.segment(text)
    except Exception:
        sents = [text.strip()]
    sents = [s.strip() for s in sents if s.strip()]
    return ' '.join(sents[:max_sentences])

def write_formatted(messages: List[Message], out_path: str):
    with open(out_path, 'w', encoding='utf-8') as f:
        for idx, m in enumerate(messages):
            if m.role == 'Assistant':
                content = summarize_assistant(m.content, max_sentences=3)
            else:
                content = m.content.strip()
            f.write(f"{m.role}:\n")
            f.write(content + "\n")
            if idx != len(messages) - 1:
                f.write("\n---\n\n")

def main():
    try:
        raw = read_file(INPUT_FILE)
    except FileNotFoundError:
        sys.exit(f"Input file not found: {INPUT_FILE}")
    messages = parse_messages(raw)
    if not messages:
        sys.exit("No messages parsed from input")
    write_formatted(messages, OUTPUT_FILE)

if __name__ == "__main__":
    main()

