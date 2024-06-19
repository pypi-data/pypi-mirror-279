"""
Redefine command line tool (enable python -m redefine syntax)
"""

import sys


def main() -> None:  # needed for console script
    if not __package__:
        # To be able to run 'python redefine-<version>.whl/wheel':
        import os.path

        path = os.path.dirname(os.path.dirname(__file__))
        sys.path[0:0] = [path]
    import redefine

    sys.exit(redefine.execute_from_cmd())


if __name__ == "__main__":
    main()
