# mgallery: A CLI Tool for Creating Static HTML Galleries

## Overview

mgallery is a command-line interface (CLI) tool that helps you create static HTML galleries from your images and text files. With mgallery, you can easily combine your files into a single HTML file, to view your gallery. It has similar style to twitter tweets.

## Installation

```
pip install mgallery
```

## Features

- Combine images (PNG, JPEG) and text files into a single HTML file
- Add or replace datetime metadata of images with current datetime
- Add or replace note metadata of images with a given note
- Read datetime and note metadata of images
- Supports multiple input files and directories

## Usage:

### Compile Command

Compile images and text files into a single HTML file:
```
mgallery compile <input_files> [-o output_file]
```

Example:

```
mgallery compile -o /tmp/output.html
```

If not given `input_files`, then it will consider current working directory files as input.

### Datetime Command

Add or replace datetime metadata of an image with current datetime:
```
mgallery datetime <image_filename>
```

### Note Command

Add or replace note metadata of an image with a given note:
```
mgallery note <image_filename> <note>
```

### Read Command

Read datetime and note metadata of an image:
```
mgallery read <image_filename>
```

## License

mgallery is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgments

I would like to thank the following projects and libraries that helped me create mgallery:

- vercel v0
- Groq LLaMA 70b
- Tailwind
- Pillow (PIL)
- Python standard libraries

## Issues

If you encounter any issues or have feedback, please open an issue in this repository.

I hope this helps! Let me know if you need any further modifications.
