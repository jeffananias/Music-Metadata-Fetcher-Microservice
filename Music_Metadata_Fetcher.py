# Group: The Abstraction Layer
# Course: CS361
# Assignment: 9 - Big Pool Implementation
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
    print('Request is 1-line string of absolute path to music file.')
    print('Response is 4-line string of artist, album, genre, and year.\n')


def get_file_text() -> str:
    """
    Return text from REQUEST FILE if exists; else, create empty file and
    return empty string.
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
    Return true if text from REQUEST FILE exists, does not match the last
    file text, and has only one newline; else, return false.
    """
    newline_count = len(file_text.split('\n'))
    if file_text != '' and file_text != last_file_text and newline_count == 1:
        return True
    else:
        return False


def process_metadata(song_path: str) -> str:
    """
    Return string of artist, album, genre, and year tags on new lines
    based on metadata of the song file in the input path.
    """
    tag: TinyTag = TinyTag.get(song_path)
    return f'{tag.artist}\n{tag.album}\n{tag.genre}\n{tag.year}'


def process_request(file_text: str, last_file_text: str) -> str:
    """
    Return response based on request or return original file text if the
    request is invalid.
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
    Start microservice as a continuous process.
    """
    greet()

    last_file_text = ''
    while True:
        file_text = get_file_text()
        last_file_text = process_request(file_text, last_file_text)
        time.sleep(1)


if __name__ == '__main__':
    run_microservice()
