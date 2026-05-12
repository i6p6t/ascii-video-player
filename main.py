import cv2
import shutil
import time
import sys
import threading
import subprocess
import numpy as np

ASCII_CHARS = " .,:;irsXA253hMHGS#9B&@"

FPS_LIMIT = 30
CHAR_RATIO = 0.55

def hide_cursor():
    print("\033[?25l", end="")

def show_cursor():
    print("\033[?25h", end="")

def move_home():
    print("\033[H", end="")

def clear_screen():
    print("\033[2J\033[H", end="")

def play_audio(video_path):
    subprocess.run(
        ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", video_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def get_terminal_size():
    return shutil.get_terminal_size((120, 40))

def get_ascii_dimensions(frame_shape, term_width, term_height):
    h, w = frame_shape

    width = term_width
    height = int((h / w) * width * CHAR_RATIO)

    if height > term_height:
        height = term_height
        width = int((w / h) * height / CHAR_RATIO)

    width = term_width
    height = min(height, term_height)

    return width, height

def frame_to_ascii(frame, width, height):

    frame = cv2.convertScaleAbs(frame, alpha=1.3, beta=10)

    blur = cv2.GaussianBlur(frame, (0, 0), 2)
    frame = cv2.addWeighted(frame, 1.5, blur, -0.5, 0)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gamma = 0.8
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
    gray = cv2.LUT(gray, table)

    gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_AREA)
    color = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

    lines = []

    for y in range(height):
        line = []

        for x in range(width):
            pixel = gray[y, x]

            char = ASCII_CHARS[int(pixel / 255 * (len(ASCII_CHARS) - 1))]

            line.append((char, color[y, x]))

        raw = "".join([c for c, _ in line])

        raw = raw[:width].ljust(width)

        colored_line = ""

        for i in range(width):
            char, (b, g, r) = line[i]
            colored_line += f"\033[38;2;{r};{g};{b}m{char}\033[0m"

        lines.append(colored_line)

    return "\n".join(lines)

if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} video.mp4")
    sys.exit()

video_path = sys.argv[1]

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Failed to open video")
    sys.exit()

fps = cap.get(cv2.CAP_PROP_FPS)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

if fps <= 0:
    fps = FPS_LIMIT

frame_delay = 1 / min(fps, FPS_LIMIT)

threading.Thread(target=play_audio, args=(video_path,), daemon=True).start()

current = 0
start = time.time()

hide_cursor()
clear_screen()

try:
    while True:
        t0 = time.time()

        ret, frame = cap.read()
        if not ret:
            break

        current += 1

        tw, th = get_terminal_size()
        w, h = get_ascii_dimensions(frame.shape[:2], tw, th)

        ascii_frame = frame_to_ascii(frame, w, h)

        move_home()
        sys.stdout.write(ascii_frame)
        sys.stdout.flush()

        elapsed = time.time() - start
        fps_now = current / elapsed if elapsed > 0 else 0
        progress = (current / total) * 100

        sys.stdout.write(f"\x1b]2;6p6t | {progress:.1f}% | {fps_now:.1f} FPS\x07")

        sleep = frame_delay - (time.time() - t0)
        if sleep > 0:
            time.sleep(sleep)

except KeyboardInterrupt:
    pass

finally:
    cap.release()
    show_cursor()
    print("\033[0m")

import os
os.system("cls")
