import os
from bs4 import BeautifulSoup #pip install beautifulsoup4

#Find html file. The script assumes there is only one html file in the folder and just uses the first one it finds
def find_html_file():
    for file in os.listdir():
        if file.endswith(".html"):
            return file
    return None

#Extract ChatGPT responses from the HTML file
def extract_chatgpt_responses(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        responses = soup.find_all('div', {'data-message-author-role': 'assistant'}) #ChatGPT's responses are identified via this tag
        return [response.get_text(separator='\n', strip=True) for response in responses if response.get_text(separator='\n', strip=True)]

#Write responses to a text file
def write_responses_to_file(responses, output_file='chatgpt_responses.txt'):
    with open(output_file, 'w', encoding='utf-8') as file:
        for response in responses:
            file.write(response + '\n\n')

#Main script logic
html_file = find_html_file()
if html_file:
    responses = extract_chatgpt_responses(html_file)
    if responses:
        write_responses_to_file(responses)
        print(f"Extracted {len(responses)} responses and wrote them to chatgpt_responses.txt")
    else:
        print("No responses found in the HTML file.")
else:
    print("No HTML file found in the current directory.")
