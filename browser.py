import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style


def text_from_tag(tag):
    if tag.name == 'a':
        return Fore.BLUE + tag.get_text() + Style.RESET_ALL
    return tag.get_text()


args = sys.argv
assert len(args) > 1

tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']

save_dir = args[1]
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

saved = []

history = deque()
last_site = ""

while True:
    command = input()

    if command == 'exit':
        sys.exit()
    elif command == 'back':
        with open(f"{save_dir}/{history.pop()}") as saved_url:
            print(saved_url.read())
        continue

    if command in saved:
        with open(f"{save_dir}/{command}", 'r', encoding='utf-16') as saved_url:
            print(saved_url.read())
        history.append(last_site)
        last_site = command
        continue
    elif '.' not in command:
        print("error: invalid url")
        continue

    save_file_name = command.rsplit('.', 1)[0]
    if save_file_name.startswith('https://'):
        save_file_name = save_file_name[8:]
    saved.append(save_file_name)

    url = command if command.startswith('https://') else 'https://' + command
    resp = requests.get(url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        tags_with_text = soup.find_all(tags)
        text = '\n'.join(map(text_from_tag, tags_with_text))
        with open(f"{save_dir}/{save_file_name}", 'w', encoding='utf-16') as save_file:
            save_file.write(text)
        print(text)
        history.append(last_site)
        last_site = save_file_name
    else:
        print("error: invalid url")
