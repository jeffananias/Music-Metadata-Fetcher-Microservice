# Group: The Abstraction Layer
# Course: CS361
# Assignment: 7 - Big Pool Implementation
# Microservice: Music Metadata Fetcher
# Due Date: 2026-08-10

from tinytag import TinyTag
import time


REQUEST_FILE = 'music_metadata.txt'


def greet() -> None:
    """
    Greet user and advise request-response format.
    """
    print('\nMusic Metadata Fetcher Microservice is running.')
    print('Waiting for metadata request in music_metadata.txt.')
    print('Request must be a music file path.')
    print('Response is a 4-tuple of artist, album, genre, and year.\n')


def get_file_text() -> str:
    """
    TODO: Write docstring
    """
    try:
        with open(REQUEST_FILE, 'r') as f:
            file_text = f.read().strip()
    except FileNotFoundError:
        with open(REQUEST_FILE, 'w') as f:
            f.write('')
        file_text = ''
    
    return file_text


def validate_request(file_text: str, last_file_text: str) -> bool:
    """
    TODO: Write docstring
    """
    newline_count = len(file_text.split('\n'))
    if file_text != '' and file_text != last_file_text and newline_count == 1:
        return True
    else:
        return False


def process_metadata(song_path: str) -> str:
    """
    TODO: Write docstring
    """
    tag: TinyTag = TinyTag.get(song_path)
    return f'{tag.artist}\n{tag.album}\n{tag.genre}\n{tag.year}'


def process_request(file_text: str, last_file_text: str) -> str:
    """
    TODO: Write docstring
    """
    if validate_request(file_text, last_file_text) is True:
        print('Request received: ' + file_text)
        response = process_metadata(file_text)
        with open(REQUEST_FILE, 'w') as f:
            f.write(response)
        print('Response sent: \n' + response)
        return response
    else:
        return file_text


def run_microservice() -> None:
    """
    TODO: Write docstring
    """
    greet()

    last_file_text = ''
    while True:
        file_text = get_file_text()
        last_file_text = process_request(file_text, last_file_text)
        time.sleep(1)

if __name__ == '__main__':
    run_microservice()
