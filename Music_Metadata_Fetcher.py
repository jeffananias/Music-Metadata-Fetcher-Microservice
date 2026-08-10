# Group: The Abstraction Layer
# Course: CS361
# Assignment: 9 - Big Pool Implementation
# Microservice: Music Metadata Fetcher
# Due Date: 2026-08-10

from tinytag import TinyTag
import time


REQUEST_FILE = "music_metadata.txt"


def greet() -> None:
    """
    Greet user and advise request-response format.
    """
    print("\nMusic Metadata Fetcher Microservice is running.")
    print("Waiting for metadata request in music_metadata.txt.")
    print("Request is string of one or more absolute paths to music files.")
    print("Response is string of groups of artist, album, genre, year.\n")


def get_file_text() -> str:
    """
    Return text from REQUEST FILE if exists; else, create empty file and
    return empty string.
    """
    try:
        with open(REQUEST_FILE, "r") as f:
            file_text = f.read().strip()
    except FileNotFoundError:
        with open(REQUEST_FILE, "w") as f:
            f.write("")
        file_text = ""
    
    return file_text


def validate_request(file_text: str, last_file_text: str) -> bool:
    """
    Return true if text from REQUEST FILE exists and does not match the last
    file text; else, return false.
    """
    if file_text != "" and file_text != last_file_text:
        return True
    else:
        return False


def get_song_paths() -> list:
    """
    Return list of absolute paths to music files based on file text.
    """
    song_paths = []
    with open(REQUEST_FILE, "r") as f:
        song_paths = f.read().splitlines()
    return song_paths


def process_metadata(song_paths: list) -> str:
    """
    Return string of artist, album, genre, and year tags on new lines
    based on metadata of the song file in the input path.
    """
    metadata = ""
    for song_path in song_paths:
        tag: TinyTag = TinyTag.get(song_path)
        metadata = metadata + \
            f"{tag.artist}\n{tag.album}\n{tag.genre}\n{tag.year}\n"
    return metadata[:-1]


def process_request(file_text: str, last_file_text: str) -> str:
    """
    Return response based on request or return original file text if the
    request is invalid.
    """
    if validate_request(file_text, last_file_text) is True:
        print("Request received: " + file_text)
        song_paths = get_song_paths()
        response = process_metadata(song_paths)
        with open(REQUEST_FILE, "w") as f:
            f.write(response)
        print("Response sent: \n" + response)
        return response
    else:
        return file_text


def run_microservice() -> None:
    """
    Start microservice as a continuous process.
    """
    greet()

    last_file_text = ""
    while True:
        file_text = get_file_text()
        last_file_text = process_request(file_text, last_file_text)
        time.sleep(1)


if __name__ == "__main__":
    run_microservice()
