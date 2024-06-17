from typing import Optional

class Song:
    def __init__(self, reference: str, artist: str, title: str, lyrics: str) -> None:
        self.reference: str = reference
        self.artist: str = artist
        self.title: str = title
        self.lyrics: str = lyrics

    def form(self) -> str:
        # returns the object data as a string
        return f'{self.artist}\0{self.title}\0{self.lyrics}'

    def compress(self) -> bytes:
        import zlib

        # returns the gzip compressed data
        return zlib.compress(self.form().encode())

    def save(self) -> None:
        import os

        from . import paths

        # gets the name of the data file from reference and generates its directory
        file_name: str = os.path.join(paths.data, *self.reference.split('/'))
        os.makedirs(os.path.dirname(file_name), exist_ok = True)

        # saves the compressed data into the file
        with open(file_name, 'wb') as file:
            file.write(self.compress())


def get_song(reference: str) -> Optional[Song]:
    import requests
    import bs4

    # gets the URL of the lyrics from AZLyrics
    url: str = f'https://www.azlyrics.com/lyrics/{reference}.html'

    # sends HTTP request for the lyrics page
    response: requests.Response = requests.get(url)

    # if the response is success
    if response.status_code == 200:
        # parses the lyrics page
        page: bs4.BeautifulSoup = bs4.BeautifulSoup(response.content, 'html.parser')

        # looks for the lyrics, artist, and title of the song
        lyrics: str = page.find('div', attrs = {'class': None, 'id': None}).get_text().strip()
        artist: str = page.find('b').get_text().rsplit(' ', 1)[0]
        title: str = page.find_all('b')[1].get_text().strip('"')

        # returns a Song object with its information
        return Song(reference, artist, title, lyrics)

    else:
        return None


def open_song(reference: str) -> Optional[Song]:
    import os
    import zlib

    from . import paths

    # gets the name of the data file
    file_name: str = os.path.join(paths.data, *reference.split('/'))

    # if the file exists
    if os.path.exists(file_name):
        # decompresses and parses the file
        with open(file_name, 'rb') as file:
            data: bytes = zlib.decompress(file.read())
            contents: list[str] = data.decode().split('\0')

        # returns the content as a Song object
        return Song(reference, *contents)

    else:
        return None
