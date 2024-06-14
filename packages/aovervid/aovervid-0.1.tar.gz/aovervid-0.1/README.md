# Aovervid

Aovervid is a Python script for overlaying audio onto video files using ffmpeg. It provides a command-line interface to merge audio and video seamlessly.

## Installation

You can install Aovervid using pip:

```bash
pip install aovervid


Make sure you have ffmpeg installed on your system. You can download it from ffmpeg.org and follow the installation instructions for your platform.

Usage
To use Aovervid, run the following command:

aovervid




Follow the prompts to enter the paths to your input video file, overlay audio file, and specify the output video file path. You can adjust the volume levels of the original audio and overlay audio, and choose to use the -shortest option to match the duration of the shortest input file.

Example
Here's an example of using Aovervid:

aovervid


Enter the input video file path: /path/to/input_video.mp4
Enter the overlay audio file path: /path/to/overlay_audio.mp3
Enter the output video file path: /path/to/output_video.mp4
Specify the original audio volume (default 100%): 100
Specify the overlay audio volume (default 50%): 50
Use -shortest option to match duration (y/n): y

Author
Made by Avinion
Telegram: @akrim