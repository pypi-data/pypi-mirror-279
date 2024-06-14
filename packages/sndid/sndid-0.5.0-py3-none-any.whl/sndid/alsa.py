# sndid/alsa.py
# Copyright 2023, 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0

import argparse
import subprocess
from pydantic import BaseModel, validator


class ArgsModel(BaseModel):
    """Model for command-line arguments

    Attributes:
        ip (str): IP address to stream to. Default is 127.0.0.1.
        port (int): Port to stream to. Default is 9988.
        rate (int): Sample rate. Default is 48000.
        time (int): Duration to stream for. Default is 10.

    Validators:
        validate_int_values: Validates that integer values are positive.
    """

    ip: str = "127.0.0.1"
    port: int = 9988
    rate: int = 48000
    time: int = 10

    @validator("port", "rate", "time")
    def validate_int_values(cls, v):
        if v < 0:
            raise ValueError("Integer values must be positive")
        return v


def parse_args() -> ArgsModel:
    """Parse command-line arguments and return ArgsModel instance"""
    parser = argparse.ArgumentParser(description="Run sndid-alsa")
    args = parser.parse_args()
    return ArgsModel(**vars(args))


def run_alsa_stream(ip: str, port: int, rate: int, time: int):
    """Run ALSA stream to specified IP address and port with given sample rate and duration

    Args:
        ip (str): IP address to stream to.
        port (int): Port to stream to.
        rate (int): Sample rate.
        time (int): Duration to stream for.

    The `run_alsa_stream` function takes in the IP address, port, sample rate, and duration
    as arguments and runs an ALSA stream to the specified IP address and port with the given
    sample rate and duration.

    The function constructs a command that uses `arecord` to record audio input and `nc` (netcat)
    to send the audio data to the specified IP address and port. The command is run using
    the `subprocess.run` function.

    """
    command = [
        "arecord",
        "--rate",
        str(rate),
        "-f",
        "FLOAT_LE",
        "--max-file-time",
        str(time),
        "|",
        "nc",
        ip,
        str(port),
    ]
    print(f"Streaming ALSA in to {ip}:{port}")
    subprocess.run(" ".join(command), shell=True)


def main():
    """Main function to parse arguments and run ALSA stream"""
    args = parse_args()
    run_alsa_stream(args.ip, args.port, args.rate, args.time)


if __name__ == "__main__":
    main()
