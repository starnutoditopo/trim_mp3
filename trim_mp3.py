#!/usr/local/bin/python

"""
A naive script to trim leading and trailing silence parts from MP3 files.
Based on https://gist.github.com/vivekhaldar/595af6c6aa06ed061f6f3f6c97d087c3
"""

import glob
import sys
import getopt
import os
import math
from moviepy.editor import AudioFileClip


def find_speaking(audio_clip, window_size=0.1, volume_threshold=0.01):
    """
    Iterate over audio to find the non-silent parts.
    Outputs a list of (speaking_start, speaking_end) intervals.
    Args:
        window_size: (in seconds) hunt for silence in windows of this size
        volume_threshold: volume below this threshold is considered to be silence
    """
    # First, iterate over audio to find all silent windows.
    num_windows = math.floor(audio_clip.end / window_size)
    window_is_silent = []
    for i in range(num_windows):
        s = audio_clip.subclip(i * window_size, (i + 1) * window_size)
        v = s.max_volume()
        window_is_silent.append(v < volume_threshold)

    speaking_start = 0
    for i in range(1, len(window_is_silent)):
        e1 = window_is_silent[i - 1]
        e2 = window_is_silent[i]
        # silence -> speaking
        if e1 and not e2:
            speaking_start = i * window_size
            break

    speaking_end = audio_clip.end
    for i in range(len(window_is_silent) - 2, 0, -1):
        e1 = window_is_silent[i + 1]
        e2 = window_is_silent[i]
        # silence -> speaking
        if e1 and not e2:
            speaking_end = i * window_size
            break

    return (speaking_start, speaking_end)


def main(argv):
    "The program's entry point"
    input_files = []
    output_directory = ""
    window_size = 0.1
    volume_threshold = 0.01
    opts, _ = getopt.getopt(
        argv, "hi:o:w:v:", ["ifile=", "odir=", "wsize", "vthreshold"]
    )
    for opt, arg in opts:
        if opt == "-h":
            print(
                "trim_mp3.py -i <input_files> -o <output_directory>"
                + " -w <window_size> -v <volume_threshold>"
            )
            print("Default values:")
            print(f"   window_size: {window_size}")
            print(f"   volume_threshold: {volume_threshold}")
            sys.exit()
        elif opt in ("-i", "--ifiles"):
            input_files = glob.glob(arg)
        elif opt in ("-o", "--odir"):
            output_directory = arg
        elif opt in ("-w", "--wsize"):
            window_size = float(arg)
        elif opt in ("-v", "--vthreshold"):
            volume_threshold = float(arg)
    # print("Input files are: ", input_files)
    # print("Output directory is: ", output_directory)

    for input_file in input_files:
        _, file_name = os.path.split(input_file)
        print(f"Processing file {file_name}...")

        base_name = os.path.splitext(file_name)[0]
        new_file_name = base_name + ".mp3"
        output_file = os.path.join(output_directory, new_file_name)
        # print(f"{output_file}")

        with AudioFileClip(input_file) as clip:
            (start, end) = find_speaking(clip, window_size, volume_threshold)
            print(f"   Keeping interval: ({start}; {end})")
            trimmed_clip = clip.subclip(start, end)
            trimmed_clip.write_audiofile(output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
