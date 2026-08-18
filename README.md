# Music Metadata Fetcher Microservice

Retrieve artist, album, and year from music files.

Input: 1-line string of absolute path to music file

Example: 
```
/Users/user/Music/song.mp3
```

Output: 3-line string of artist, album, and year

Example: 
```
Beatles
Help!
1965
```

---

## Dependencies

Install tinytag >= 2.3.0 with `pip install tinytag`.
