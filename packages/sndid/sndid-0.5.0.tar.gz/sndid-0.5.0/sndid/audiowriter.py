# sndid/audiowriter.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import logging
import os
from .jack_lazy_loader import jack_lazy_load


class AudioWriter:
    """
    Class responsible for writing audio detections to disk.

    Args:
        detections_dir (str): Directory to save audio detections.

    Attributes:
        detections_dir (str): Directory to save audio detections.
    """

    def __init__(self, detections_dir):
        self.detections_dir = detections_dir
        logging.debug("Initialized AudioWriter with detections_dir: %s", detections_dir)

    def write_audio(self, recording_data, detections, detection_timestamp, input_index):
        """
        Write audio detections to disk.

        Args:
            recording_data (np.ndarray): The audio data to write.
            detections (List[Dict[str, Union[str, float]]]): List of detections,
                where each detection is a dictionary containing start_time,
                end_time, and scientific_name keys.
            detection_timestamp (datetime): The timestamp of the detection.
            input_index (int): Index of the input in the multiplexed recording.
        """
        for d in detections:
            start_sample = int(d["start_time"] * 48000)
            end_sample = int(d["end_time"] * 48000)
            logging.debug(
                "Processing detection with start_sample: %s and end_sample: %s",
                start_sample,
                end_sample,
            )
            detection_audio = recording_data[start_sample:end_sample]
            species_dir = os.path.join(
                self.detections_dir,
                f"input_{input_index + 1}",
                d["scientific_name"].lower().replace(" ", "_"),
            )

            logging.debug("species_dir: %s", species_dir)
            os.makedirs(species_dir, exist_ok=True)
            detection_filename = f"{d['scientific_name'].lower().replace(' ', '_')}_{detection_timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.wav"
            detection_filepath = os.path.join(species_dir, detection_filename)
            logging.debug("detection_filepath: %s", detection_filepath)
            wavfile = jack_lazy_load("scipy.io.wavfile")
            wavfile.write(detection_filepath, 48000, detection_audio)
            logging.debug("Audio file written: %s", detection_filename)
