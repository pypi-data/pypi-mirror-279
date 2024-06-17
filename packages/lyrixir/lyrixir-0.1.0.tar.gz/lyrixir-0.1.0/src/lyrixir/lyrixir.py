from typing import Optional

import random

from . import config
from . import fancy
from . import songs


def print_section(section: str, content: str) -> None:
    # calls the custom fancy print based on configuration
    fancy.prepare_print(
        config.configuration[section]['alignment'],
        config.configuration[section]['color'],
        config.configuration[section]['styles'],
    )(content)


def print_song(song: songs.Song) -> None:
    # splits the lyrics into chunks based on the scale configuration
    chunks: list[str] = []
    match config.configuration['lyrics']['scale']:
        case 'line':
            chunks = [line for line in song.lyrics.splitlines() if line]
        case 'stanza':
            chunks = song.lyrics.split('\n\n')
        case 'song':
            chunks = [song.lyrics]

    # if the chunks are valid, prints a random chunk of the lyrics
    if chunks:
        lyrics: str = random.choice(chunks)
        print_section('lyrics', lyrics)

    # prints error if configuration is invalid
    else:
        fancy.print_error("unrecognized scale in config file")

    # loops for each included information in the configuration
    for element in config.configuration['info']['include']:
        # grabs the information
        information: str = ''
        match element:
            case 'artist': information = song.artist
            case 'title': information = song.title

        # prints the information if the information is valid
        if information:
            print_section('info', information)

        # prints error if configuration is invalid
        else:
            fancy.print_error("unrecognized include in config file")


def pick_song() -> Optional[songs.Song]:
    # gets the reference list
    reference_list: list[str] = config.read_reference_list()

    # picks a random reference
    random_reference: str = random.choice(reference_list)

    # returns the song object of the random reference
    return songs.open_song(random_reference)


def main() -> None:
    # gets a random song
    song: Optional[songs.Song] = pick_song()

    # keep trying if it fails
    while not song:
        song = pick_song()

    # prints the song lyrics and information
    print_song(song)
