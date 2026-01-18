import os
from bs4 import BeautifulSoup
import settings

def find_html_file():
    for file in os.listdir():
        if file.endswith(".html"):
            return file
    return None

def extract_responses(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        responses = soup.find_all('div', {'data-message-author-role': 'assistant'})
        return [response.get_text(separator='\n', strip=True) for response in responses if response.get_text(separator='\n', strip=True)]

def write_responses_to_file(responses, output_file=settings.OUTPUT_FILE):
    with open(output_file, 'w', encoding='utf-8') as file:
        for response in responses:
            file.write(response + '\n\n')

def main():
    html_file = find_html_file()
    if html_file:
        responses = extract_responses(html_file)
        if responses:
            write_responses_to_file(responses)
            print(f"Extracted {len(responses)} responses and wrote them to {settings.OUTPUT_FILE}")
        else:
            print("No responses found in the HTML file.")
    else:
        print("No HTML file found in the current directory.")

if __name__ == "__main__":
    main()

