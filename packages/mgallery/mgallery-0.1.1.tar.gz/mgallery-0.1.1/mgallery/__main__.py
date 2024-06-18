import argparse
from pathlib import Path

from PIL import Image

from .htmlcreator import html_combine, image_html, txt_html


def get_items(dir: Path):
    temp = []
    for k in dir.iterdir():
        if k.is_dir() == True:
            temp += get_items(k)
        elif k.suffix in [".png", ".jpeg", ".txt", ".jpg"]:
            temp.append(k)
    return temp


def compile(inputs: list[str], output_path: str | None):
    files = []
    for inp in inputs:
        pat = Path(inp)
        if pat.exists() == False:
            raise Exception(f"{inp} file/directory doesn't exists")

        if pat.is_dir() == True:
            files += get_items(pat)
        elif pat.suffix in [".png", ".jpeg", ".txt", ".jpg"]:
            files.append(pat)

    # now sorting them
    files = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)

    htmls_values = []
    for f in files:
        filetype = f.suffix
        if filetype == ".txt":
            htmls_values.append(txt_html(f))
        else:
            htmls_values.append(image_html(f))

    html_result = html_combine(htmls_values)

    outpt = "output.html" if output_path == None else output_path
    with open(outpt, "w") as f:
        f.write(html_result)

    return


def read_note(image_filename: str):
    with Image.open(image_filename) as img:
        exif_dict = img.getexif()
    if (
        270 in exif_dict
        and all(byte == 0 for byte in exif_dict[270].encode("ascii")) == False
    ):
        print(f"note:\n{exif_dict[270]}")
    else:
        print("No Note attached")
    return


def add_replace_note(image_filename: str, note: str):
    with Image.open(image_filename) as img:
        exif_dict = img.getexif()
        exif_dict[270] = note
        img.save(image_filename, exif=exif_dict)
    return


def main():
    global_parser = argparse.ArgumentParser(
        prog="mgallery",
        description="cli tools to create static html file to view gallery of text and images",
        epilog="Thanks for using %(prog)s! :)",
    )

    subparsers = global_parser.add_subparsers(
        title="commands", dest="commands", help="mgallery tools"
    )

    # note subcommand
    arn_parser = subparsers.add_parser(
        "note", help="add or replace note metadata of image with given note"
    )
    arn_parser.add_argument(
        dest="image_filename",
        type=str,
        nargs=1,
        metavar="image_filename",
        help="image file path",
    )
    arn_parser.add_argument(
        dest="note",
        type=str,
        nargs=1,
        metavar="note",
        help="note to add",
    )
    arn_parser.set_defaults(func=add_replace_note)

    # read exif subcommand
    rdn_parser = subparsers.add_parser("read", help="prints out note metadata of image")
    rdn_parser.add_argument(
        dest="image_filename",
        type=str,
        nargs=1,
        metavar="image_filename",
        help="image file path",
    )
    rdn_parser.set_defaults(func=read_note)

    # compile subcommand
    com_parser = subparsers.add_parser(
        "compile", help="combines txt and png/jpeg file to create gallery"
    )
    com_parser.add_argument(
        dest="inputs",
        type=str,
        nargs="*",
        metavar="filenames",
        default=".",
        help="name of files and directories",
    )
    com_parser.add_argument(
        "-o",
        "--output",
        dest="outputpath",
        type=str,
        nargs=1,
        metavar="output_file",
        help="path to where to save output html",
    )
    com_parser.set_defaults(func=compile)

    args = global_parser.parse_args()

    if args.commands == None:
        print("usage: mgallery -h")
    elif args.commands == "note":
        args.func(args.image_filename[0], args.note[0])
    elif args.commands == "read":
        args.func(args.image_filename[0])
    elif args.commands == "compile":
        outpt = None if args.outputpath is None else args.outputpath[0]
        args.func(args.inputs, outpt)
