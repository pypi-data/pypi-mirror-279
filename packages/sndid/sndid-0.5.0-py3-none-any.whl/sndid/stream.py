# sndid/stream.py
# Copyright 2023, 2024 Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import argparse
import signal
import subprocess
import sys


def signal_handler(signum, frame):
    """Handles the SIGINT signal by printing a message and exiting the program."""
    print("\nReceived signal to exit. Cleaning up...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def run_ffmpeg_command(ip, port, time, url):
    """Runs the ffmpeg command with subprocess, handling piping correctly.

    Args:
        ip (str): Server IP address. Default is "127.0.0.1".
        port (int): Server network port. Default is 9988.
        time (int): Length of segments in seconds. Default is 60.
        url (str): Input url. Required.

    Raises:
        CalledProcessError: If the ffmpeg process returns a non-zero exit code.
    """
    ffmpeg_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "quiet",
        "-i",
        url,
        "-acodec",
        "pcm_s16le",
        "-ac",
        "1",
        "-vcodec",
        "vnull",
        "-f",
        "wav",
        "-t",
        time,
        "-",
    ]

    nc_cmd = ["nc", "-q", "0", ip, port]

    ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE)
    subprocess.run(nc_cmd, stdin=ffmpeg_process.stdout, text=True)
    ffmpeg_process.wait()

    if ffmpeg_process.returncode != 0:
        raise subprocess.CalledProcessError(ffmpeg_process.returncode, ffmpeg_cmd)


def main():
    """Runs the sndid-stream command line interface."""
    parser = argparse.ArgumentParser(description="Run sndid-stream")
    parser.add_argument(
        "-i",
        "--ip",
        help="Server IP address (default 127.0.0.1)",
        type=str,
        required=False,
        default="127.0.0.1",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="Server network port (default 9988)",
        type=int,
        required=False,
        default="9988",
    )
    parser.add_argument(
        "-t",
        "--time",
        help="Length of segments in seconds (default 60)",
        type=int,
        required=False,
        default="60",
    )
    parser.add_argument("-u", "--url", help="Input url", type=str, required=True)

    args = parser.parse_args()
    IP = args.ip
    PORT = str(args.port)
    TIME = str(args.time)
    URL = args.url

    try:
        while True:
            print("Sending stream...")
            run_ffmpeg_command(IP, PORT, TIME, URL)
    except KeyboardInterrupt:
        print("Exiting on user interrupt.")
    finally:
        print("Script exit cleanup.")


if __name__ == "__main__":
    main()
