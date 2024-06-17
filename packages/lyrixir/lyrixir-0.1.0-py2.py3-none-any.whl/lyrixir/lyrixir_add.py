from typing import Optional

from . import config
from . import fancy
from . import songs


def add_song(reference: str) -> None:
    # tries to get the song from the reference
    try:
        song: Optional[songs.Song] = songs.get_song(reference)

    # gives error if failed
    except:
        fancy.print_error(f"unable to connect")

    else:
        # if song is gotten
        if song:
            # saves the song data and adds reference to the reference list
            song.save()
            config.add_to_reference_list(reference)

            fancy.print_success(f"added {song.title} by {song.artist}")
        else:
            fancy.print_error(f"{reference} is unavailable")


def add_songs(references: list[str]) -> None:
    # gets the reference list
    reference_list: list[str] = config.read_reference_list()

    # loops for each entered references
    for song_reference in references:
        # adds song if it isn't on the reference list
        if song_reference in reference_list:
            fancy.print_neutral(f"{song_reference} is already added")
        else:
            add_song(song_reference)


def main(arguments: list[str]) -> None:
    # makes sure references were given as arguments
    if arguments:
        add_songs(arguments)
    else:
        fancy.print_error("no song reference entered")
