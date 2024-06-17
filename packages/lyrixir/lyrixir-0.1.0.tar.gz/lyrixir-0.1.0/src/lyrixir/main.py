import sys


def main() -> None:
    # gets the command line arguments
    arguments: list[str] = sys.argv[1:]

    # if any arguments were given
    if arguments:
        # gets first argument as command
        command: str = arguments[0]

        # matches and runs respective command
        match command:
            case 'add':
                from . import lyrixir_add
                lyrixir_add.main(arguments[1:])

            case 'list':
                from . import lyrixir_list
                lyrixir_list.main(arguments[1:])

            case 'remove':
                from . import lyrixir_remove
                lyrixir_remove.main(arguments[1:])

            case _:
                pass

    # if no arguments were given
    else:
        # runs lyrixir
        from . import lyrixir
        lyrixir.main()
