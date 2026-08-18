# Group: The Abstraction Layer
# Course: CS361
# Assignment: 9 - Big Pool Implementation
# Microservice: Music Metadata Fetcher
# Due Date: 2026-08-10

import time

import tinytag

REQUEST_FILE = "music_metadata.txt"


def main() -> None:
    """Start microservice as continuous process."""
    greet()
    last_file_text = ""
    while True:
        file_text = get_file_text()
        last_file_text = process_request(file_text, last_file_text)
        time.sleep(0.5)


def greet() -> None:
    """Greet user and advise request-response format."""
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


def process_request(file_text: str, last_file_text: str) -> str:
    """
    Return response based on request or return original file text if
    request is invalid.
    """
    if file_text != "" and file_text != last_file_text:
        if is_response_message(file_text):
            return file_text
        else:
            print("Request received: " + file_text)
            song_paths = get_song_paths()
            response = process_metadata(song_paths)
            with open(REQUEST_FILE, "w") as f:
                f.write(response)
            print("Response sent:\n" + response)
            return response
    return last_file_text


def is_response_message(file_text: str) -> bool:
    """
    Return True if file_text is response instead of request;
    else return False.
    """
    file_lines = file_text.split("\n")
    music_exts = (".mp3", ".wav", ".flac", ".aac", ".ogg")
    return bool(file_lines[0].endswith(music_exts) is False)


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
    based on metadata of song file in input path.
    """
    metadata = ""
    for song_path in song_paths:
        tag: tinytag.TinyTag = tinytag.TinyTag.get(song_path)
        metadata = metadata + f"{tag.artist}\n{tag.album}\n{tag.year}\n"
    return metadata[:-1]


if __name__ == "__main__":
    main()
