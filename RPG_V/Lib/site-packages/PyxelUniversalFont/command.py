import argparse

from .sample_app import start_app
from .src.root import edit_fonts

cmd_dict = {
    "sample": start_app,
    "edit": edit_fonts,
}

def command_manager():
    parser = argparse.ArgumentParser(description="A command-line interface for the pyxel-universal-font library. Easily sample or edit fonts.")
    parser.add_argument('cmd', type=str, choices=cmd_dict.keys(), help='Specify the operation to perform. "sample" to start the sample application. "edit" to edit fonts.')
    args = parser.parse_args()
    cmd_dict[args.cmd]()
    