"""Boggler Demo"""
import argparse
import json
from itertools import chain
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box
from .boggler_utils import BoggleBoard, build_full_boggle_tree, read_boggle_file

parser = argparse.ArgumentParser(prog="boggler", description="Boggle board game solver")

parser.add_argument("board", type=Path, help="Path to board CSV file")
parser.add_argument(
    "wordlists",
    type=Path,
    help='Path to directory of wordlist files. The directory must contain \
        text files of the form words_X.txt where "X" is a character of \
        the alphabet',
)
parser.add_argument(
    "max_word_length",
    nargs="?",
    type=int,
    default=16,
    help="Maximum length of words searched for on provided board",
)
parser.add_argument(
    "-f",
    "--format",
    type=str,
    help="Specify alternative output format including [txt, json]",
)
parser.add_argument(
    "-p",
    "--include-path",
    action="store_true",
    default=False,
    help="Include full paths for each word in output",
)
parser.add_argument(
    "-s",
    "--sort",
    action="store_true",
    default=False,
    help="Sort output alphabetically. By default the results are sorted by the starting \
          block position on the board from top-to-bottom, left-to-right as given in the \
          board file.",
)
parser.add_argument(
    "-d",
    "--dedup",
    action="store_true",
    default=False,
    help="Remove duplicates from word-only output. Note that de-duplication does not preserve \
          the original order of the output, so it is recommended to also use the sort option when \
          de-duplicating.",
)

args = parser.parse_args()


def main():
    """Command line tool for sovling Boggle boards"""
    board = read_boggle_file(args.board)
    try:
        boggle_board = BoggleBoard(board, args.max_word_length)
    except ValueError:
        print("Invalid MAX_WORD_LENGTH. Please try again with a valid integer.")
        sys.exit()

    boggle_tree = build_full_boggle_tree(boggle_board, Path(args.wordlists))

    if args.format:
        match args.format.lower():
            case "txt":
                word_paths = [
                    start_block.word_paths for start_block in boggle_tree.values()
                ]
                data = list(chain(*word_paths))
                if args.include_path:
                    data = [f"{line[0]} {line[1]}" for line in data]
                else:
                    data = [x[0] for x in data]
                    if args.dedup:
                        data = list(set(data))

                if args.sort:
                    data.sort()

                for line in data:
                    print(line)

            case "json":
                data = {str(k): v.word_paths for k, v in boggle_tree.items()}
                print(json.dumps(data, indent=2, sort_keys=True))
            case _:
                print(f'Invalid format (-f) option provided: "{args.format}"')
                sys.exit()

    else:
        console = Console()
        print("\nBOARD")
        print(boggle_board)

        for start_pos, tree in boggle_tree.items():
            table = Table(
                title=f"Starting @ {start_pos}",
                show_header=True,
                header_style="bold purple",
                row_styles=["dim", ""],
                box=box.ROUNDED,
            )
            table.add_column("Word")
            table.add_column("Path")
            for word in tree.word_paths:
                # print(f"{word[0]: <{boggle_board.max_word_len}}: {word[1]}")
                table.add_row(f"{word[0]}", f"{word[1]}")

            console.print(table)


if __name__ == "__main__":
    main()
