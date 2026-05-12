<div align="center">

# ASCII Video Player

Real-time terminal video rendering using colored ASCII characters and synchronized audio.

<img src="https://img.shields.io/badge/python-3.9+-black?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/opencv-supported-black?style=for-the-badge">
<img src="https://img.shields.io/badge/platform-windows%20%7C%20linux-black?style=for-the-badge">

</div>

---

## Overview

ASCII Video Player is a high-performance terminal-based media renderer written in Python.

It converts video frames into dynamically colored ASCII characters in real time while playing synchronized audio through FFmpeg.

Designed for smooth playback, sharp rendering, and clean terminal output.

---

## Features

- Real-time ASCII video rendering
- Full 24-bit RGB terminal coloring
- Audio playback support via FFmpeg
- Dynamic terminal scaling
- Sharpening and gamma correction
- Automatic FPS limiting
- Lightweight and dependency minimal
- ANSI terminal support

---

## Screenshot

```text
@#S39HMh23Airs;,. 
GS#9B&@hMH532Airs
XA253hMHGS#9B&@@@
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourname/ascii-video-player
cd ascii-video-player
```

## Install Dependencies

```bash
pip install opencv-python numpy
```

---

# FFmpeg Requirement

This project requires FFmpeg and ffplay installed globally.

## Windows

```bash
winget install ffmpeg
```

Verify installation:

```bash
ffmpeg -version
ffplay -version
```

---

# Usage

```bash
python main.py video.mp4
```

Example:

```bash
python main.py movie.mp4
```

---

# Technical Details

The renderer performs the following pipeline for each frame:

1. Frame extraction using OpenCV
2. Contrast enhancement
3. Gaussian sharpening
4. Gamma correction
5. Grayscale conversion
6. ASCII brightness mapping
7. RGB color reconstruction
8. Terminal rendering using ANSI escape sequences

---

# ASCII Character Ramp

```python
ASCII_CHARS = " .,:;irsXA253hMHGS#9B&@"
```

Characters are mapped from low luminance to high luminance.

---

# Recommended Terminal

Best experience on:

- Windows Terminal
- PowerShell
- WezTerm
- Alacritty
- Linux terminals with ANSI color support

Recommended minimum size:

```text
120 x 40
```

---

# Performance

Playback performance depends on:

- Terminal rendering speed
- Video resolution
- CPU performance
- FFmpeg installation
- Terminal font rendering

---

# Credits

Developed by **6p6t**

---

# License

MIT License
