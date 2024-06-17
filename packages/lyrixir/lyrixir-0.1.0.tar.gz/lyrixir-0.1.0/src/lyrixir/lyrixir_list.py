from typing import Optional

from . import config
from . import fancy
from . import songs


def print_song_information(reference: str) -> None:
    # gets the song from the reference and prints its information
    song: Optional[songs.Song] = songs.open_song(reference)
    if song:
        fancy.print_neutral(f"{song.title} - {song.artist}")


def list_songs(references: list[str]) -> None:
    # prints the information of each reference
    for reference in references:
        print_song_information(reference)


def main(arguments: list[str]) -> None:
    references: list[str]

    # if arguments were given
    if arguments:
        references = []

        # loops for reference in the reference list
        for reference in config.read_reference_list():
            # gets the artist from the reference
            artist: str = reference.split('/')[0]

            # adds the reference to references
            if artist in arguments:
                references.append(reference)

    # adds all references if no arguments were given
    else:
        references = config.read_reference_list()

    # lists the references
    list_songs(references)
