import os
import tomllib

from . import paths


# gets the path and name of the config file
config_file_name: str = os.path.join(paths.config, 'lyrixir.toml')

# sets the default configuration
configuration: dict = {
    'lyrics': {
        'scale': 'stanza',
        'alignment': 'center',
        'color': 'black',
        'styles': ['bold'],
    },
    'info': {
        'include': ['artist', 'title'],
        'alignment': 'right',
        'color': 'black',
        'styles': ['none'],
    },
}

# if the config file exists
if os.path.exists(config_file_name):
    with open(config_file_name, 'rb') as file:
        # updates the configuration with the config file
        user_configuration: dict = tomllib.load(file)
        for table in user_configuration:
            configuration[table].update(user_configuration[table])


# gets the path and name of the reference list
list_file_name = os.path.join(paths.config, 'reference.list')


def read_reference_list() -> list[str]:
    # reads the reference list as a list
    if os.path.exists(list_file_name):
        with open(list_file_name, 'r') as file:
            return file.read().splitlines()

    # returns an empty list if the reference list doesn't exist
    else:
        return []


def write_reference_list(references: list[str]) -> None:
    with open(list_file_name, 'w') as file:
        file.write('\n'.join(reference for reference in references) + '\n')


def add_to_reference_list(reference: str) -> None:
    # creates the reference list if it doesn't exist
    os.makedirs(os.path.dirname(list_file_name), exist_ok = True)

    # adds reference to the reference list
    with open(list_file_name, 'a') as file:
        file.write(f'{reference}\n')
