# sndid/client.py
# Copyright 2023, 2024 Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
from pydantic import BaseModel
import argparse
import os


class ClientArguments(BaseModel):
    """
    A class representing the command-line arguments for the sndid-client.

    Attributes:
        ip (str): The IP address of the server to connect to. Default is 127.0.0.1.
        port (int): The port number to connect to on the server. Default is 9988.
        file (str): The file to send to the server. Default is samples/mono.wav.
    """

    ip: str = "127.0.0.1"
    port: int = 9988
    file: str = "samples/mono.wav"


def parse_arguments():
    """
    Parse the command-line arguments for the sndid-client.

    Returns:
        ClientArguments: An instance of ClientArguments with the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Run sndid-client")
    parser.add_argument(
        "-i", "--ip", help="Server IP address (default 127.0.0.1)", default="127.0.0.1"
    )
    parser.add_argument(
        "-p", "--port", help="Server network port (default 9988)", default="9988"
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Input filename to process (default samples/mono.wav)",
        default="samples/mono.wav",
    )

    args = parser.parse_args()
    parsed_args = ClientArguments(ip=args.ip, port=int(args.port), file=args.file)
    return parsed_args


def main():
    """
    Run the sndid-client.

    This function parses the command-line arguments, constructs a command to send
    the specified file to the server using netcat, and then executes that command.
    """
    parsed_args = parse_arguments()
    CMD = f"cat {parsed_args.file} | nc -q 0 {parsed_args.ip} {parsed_args.port}"
    print(f"Sending {parsed_args.file} to {parsed_args.ip}:{parsed_args.port}")
    os.system(CMD)


if __name__ == "__main__":
    main()
