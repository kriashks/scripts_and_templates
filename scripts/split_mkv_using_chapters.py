## Description: A script to split an entire disc mkv into multiple episodes if it has chapter markers
# Author: Adarsh Krishnan
# Tested on Python 3.10.10

import subprocess
import os


def split_mkv(input_file, output_dir, split_option="chapters:all"):
    # Check the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Construct an output file template.
    # mkvmerge will replace a printf-style pattern (e.g. %03d) with an incrementing file number.
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_template = os.path.join(output_dir, f"{base_name}-%03d.mkv")

    # Build the command. Here we use the splitting option provided.
    command = ["mkvmerge", "--split", split_option, "-o", output_template, input_file]
    print("Running command:", " ".join(command))

    # Execute the command; check=True ensures an exception is raised if the command fails.
    subprocess.run(command, check=True)


# How to use the function:
split_mkv(
    "path to .mkv",
    "output/vol1",
    # using chapters:all will instruct mkvmerge to split at every chapter
    "chapters:all",
)
