# mgallery: A CLI Tool for Creating Static HTML Galleries

## Overview

mgallery is a command-line interface (CLI) tool that helps you create static HTML galleries from your images and text files. With mgallery, you can easily combine your files into a single HTML file, to view your gallery. It has similar style to twitter tweets.

## Installation

```
pip install mgallery
```

## Features

- Combine images (PNG, JPEG) and text files into a single HTML file
- Add or replace note metadata of images with a given note
- Read note metadata of images
- Supports multiple input files and directories

## Usage:

### Compile Command

Compile images and text files into a single HTML file:

```
mgallery compile <input_files> [-o output_file]
```

#### Example:

Let's say my diary directory is structured like this:

```
.
├── june
│   ├── 01-06-24.txt
│   ├── 04-06-24.txt
│   ├── buildspace_s5_w0.png
│   ├── IMG_20240616_191552.jpg
│   └── maybe_future_pp.jpg
└── may
    ├── 25-05-24.txt
    ├── 26-05-24.txt
```

To compile all text and image files without any exclusions, use:

```
mgallery compile -o /tmp/output.html
```

If `input_files` is not specified, the current working directory files will be used as input.

To compile only selected files, use:

```
mgallery compile june/maybe_future_pp.jpg june/01-06-24.txt -o /tmp/output.html
```

To compile files from a directory and a selected file from another directory, use:

```
mgallery compile june may/25-05-24.txt -o /tmp/output.html
```

The `-o` or `--output` flag specifies the location of the output file. If not provided, the CLI will create `output.html` in the current working directory.

### Note Command

Add or replace note metadata of an image with a given note:
```
mgallery note <image_filename> <note>
```

### Read Command

Read note metadata of an image:
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
