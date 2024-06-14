# sndid/jackmain.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
from sndidjack.sndidjack import SndIdJack
from sndidjack.config import Config


def main():
    """
    Main function for sndid-jack executable.

    Loads configuration, initializes SndIdJack, and starts the main process.
    """
    config = Config.load_config()
    sndidjack = SndIdJack(config)
    sndidjack.main()


if __name__ == "__main__":
    main()
