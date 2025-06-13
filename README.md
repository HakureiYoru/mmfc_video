# Video Player

This project provides a simple Tkinter-based video player that randomly plays short segments from videos in a selected directory.

## Features
- Randomly selects and plays a 7–8 second segment from a video file.
- Supports `.mp4`, `.avi` and `.mov` formats.
- Keeps track of played files to avoid repeats.
- Displays a placeholder image when no video is playing.
- Customisable background image located at `img/bg.png`.

## Requirements
- Python 3.8+
- [Pillow](https://pypi.org/project/Pillow/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- Tkinter (usually included with Python on Windows; on Linux you may need to install an extra package such as `python3-tk`).

Install the dependencies with:

```bash
pip install Pillow opencv-python
```

## Running
After installing the dependencies, execute:

```bash
python video_player.py
```

A window will open allowing you to select a directory containing videos. Each time you click **Random Play** the application chooses a clip from one of the files.

## Background image
The player loads a background from `img/bg.png`. Replace this file with any image (keeping the same name) to change the window background. The file is also bundled when building an executable.

## Packaging with PyInstaller
The repository includes `video_player.spec` which can be used with [PyInstaller](https://pyinstaller.org/) to create a standalone executable. Run the following command to build the program:

```bash
pyinstaller video_player.spec
```

This bundles the Python interpreter, the script, the `img` directory and other dependencies into a single executable (by default without a console window) that can be distributed to systems without Python installed.

