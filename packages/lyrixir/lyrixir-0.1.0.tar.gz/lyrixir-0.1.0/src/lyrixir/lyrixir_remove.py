import os

from . import fancy
from . import config
from . import paths


def remove_reference(reference: str) -> None:
    # replaces the reference list with reference removed
    reference_list: list[str] = config.read_reference_list()
    reference_list.remove(reference)
    config.write_reference_list(reference_list)


def remove_data(reference: str) -> None:
    # deletes the data file of the song
    file_path: str = os.path.join(paths.data, *reference.split('/'))
    if os.path.exists(file_path):
        os.remove(file_path)


def remove_songs(references: list[str]) -> None:
    # gets the reference list
    reference_list: list[str] = config.read_reference_list()

    # loops for each entered references
    for song_reference in references:
        # removes song if it is on the reference list
        if song_reference in reference_list:
            remove_reference(song_reference)
            remove_data(song_reference)
            fancy.print_success(f"removed {song_reference}")
        else:
            fancy.print_neutral(f"{song_reference} doesn't exist")


def main(arguments: list[str]) -> None:
    # makes sure references were given as arguments
    if arguments:
        remove_songs(arguments)
    else:
        fancy.print_error("no song reference entered")
