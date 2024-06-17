import os
import platform

data: str
config: str

# gets the required file paths according to the operating system
match platform.system():
    case 'Linux':
        data = f'{os.getenv('HOME')}/.local/share/lyrixir'
        config = f'{os.getenv('HOME')}/.config/lyrixir'

    case 'Windows':
        data = f'{os.getenv('APPDATA')}\\lyrixir-data'
        config = f'{os.getenv('APPDATA')}\\lyrixir'
