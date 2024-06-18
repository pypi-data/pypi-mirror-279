import datetime
import importlib.resources
from pathlib import Path

from PIL import Image


def txt_parser(txt_file: str):
    with open(txt_file, "r") as f:
        content = f.read()

    length = len(content)
    i = 0
    res = ""
    while i < length - 1:
        if content[i] == "\n":
            if content[i + 1] == "\n":
                res += "\n\n"
                i += 1
            else:
                res += " "
        else:
            res += content[i]
        i += 1
    res += "" if content[length - 1] == "\n" else content[length - 1]

    return res


def get_dt_note(image_filename: str):
    res = dict()
    with Image.open(image_filename) as img:
        exif_dict = img.getexif()
        res["datime"] = exif_dict[36867] if 36867 in exif_dict else None
        res["note"] = exif_dict[270] if 270 in exif_dict else None
    return res


def html_combine(tweets: list[str]):
    with importlib.resources.path("mgallery.javascripts", "tailwindcss.js") as p:
        with p.open("r") as f:
            tailwind_script = f.read()

    res = "<!DOCTYPE html><html lang='en'><head><title>Gallery</title><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1'>"
    res += f"<script>{tailwind_script}</script>"
    res += "<script>tailwind.config = {theme: {extend: {colors: {text_color: 'rgba(231,233,234,1.00)', border_color: 'rgb(62,65,68,1.00)',}}}}</script></head><body class='bg-black text-text_color'><div class='w-full max-w-2xl mx-auto border-x-2 border-border_color'>"
    res += f"<div class='border-b-2 border-border_color py-3 px-4'><p class='font-bold text-xl'>mgallery</p></div>"
    res += "<div class=''>"

    for tweet in tweets:
        res += tweet

    res += "</div><div class='pb-6'></div></body></html>"

    return res


def image_html(filepath: Path):
    filepathstring = str(filepath.absolute())
    d = get_dt_note(filepathstring)
    datime = d["datime"]
    note = d["note"]
    datetime_format = "%Y:%m:%d %H:%M:%S"
    datime_object = (
        None if datime == None else datetime.datetime.strptime(datime, datetime_format)
    )

    # res = "<div class='flex items-start gap-4 border-b-2 border-border_color p-6 box-border'><div class='grid gap-1'>"
    res = "<div class='border-b-2 border-border_color p-6 box-border'><div class='grid gap-1'>"
    res += "" if note == None else f"<div class='mb-4 whitespace-pre-line'>{note}</div>"
    # res += f"<img src='{filepathstring}' alt='Image' width='600' height='400' class='rounded-md object-cover' style='aspect-ratio: 600 / 400; object-fit: cover;' />"
    res += f"<img src='{filepathstring}' alt='Image' class='rounded-md object-cover' style='aspect-ratio: 600 / 400; object-fit: cover; width: 100%; height: auto;' />"
    res += (
        ""
        if datime_object == None
        else f"<time class='text-gray-500 dark:text-gray-400 text-sm' datetime='{datime_object.isoformat(timespec='milliseconds').replace('+00:00','Z')}'>{datime_object.strftime('%I:%M %p · %b %d, %Y')}</time>"
    )
    res += "</div></div>"

    return res


def txt_html(filepath: Path):
    datime_object = datetime.datetime.fromtimestamp(filepath.stat().st_mtime)
    note = txt_parser(str(filepath.absolute()))

    # res = "<div class='flex items-start gap-4 border-b-2 border-border_color p-6 box-border'><div class='grid gap-1'>"
    res = "<div class='border-b-2 border-border_color p-6 box-border'><div class='grid gap-1'>"
    res += f"<div class='mb-4 whitespace-pre-line'>{note}</div>"
    res += f"<time class='text-gray-500 dark:text-gray-400 text-sm' datetime='{datime_object.isoformat(timespec='milliseconds').replace('+00:00','Z')}'>{datime_object.strftime('%I:%M %p · %b %d, %Y')}</time>"
    res += "</div></div>"

    return res
