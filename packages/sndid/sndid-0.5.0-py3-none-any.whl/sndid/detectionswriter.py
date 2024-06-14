# sndid/detectionswriter.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import logging
import queue
import threading
from .textwriter import TextWriter
from .audiowriter import AudioWriter


class DetectionsWriter:
    """
    A class for writing detection data to file.

    This class provides a way to write detection data to both a text file and an audio file.
    It uses a queue to handle the detection data and writes the data in a separate thread.
    """

    def __init__(self, detections_file, detections_dir):
        """
        Initialize a new DetectionsWriter object.

        :param detections_file: The file to write detection text data to.
        :param detections_dir: The directory to write detection audio data to.
        """
        logging.debug("Initializing DetectionsWriter")
        self.text_writer = TextWriter(detections_file)
        self.audio_writer = AudioWriter(detections_dir)
        self.detection_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._writer_thread = threading.Thread(target=self._write_detections_loop)
        self._writer_thread.daemon = True
        logging.debug("Starting DetectionsWriter thread.")
        self._writer_thread.start()

    def write_detections(self, detections, detection_timestamp, input_index):
        """
        Add detection data to the queue.

        :param detections: A list of detections.
        :param detection_timestamp: The timestamp of the detection.
        :param input_index: The index of the input.
        """
        self.detection_queue.put((detections, detection_timestamp, input_index))
        logging.debug(f"DetectionsWriter detections added to queue: {len(detections)}")

    def _write_detections_loop(self):
        """
        A loop that continuously checks the queue for new detection data.

        When new data is available, it writes the data to the text and audio files.
        """
        while not self._stop_event.is_set():
            try:
                detections, detection_timestamp, input_index = self.detection_queue.get(
                    timeout=1
                )
                logging.debug("Detections received from queue to DetectionsWriter.")
            except queue.Empty:
                continue
            self.text_writer.write_detections(
                detections, detection_timestamp, input_index
            )

    def write_audio(self, recording_data, detections, detection_timestamp, input_index):
        """
        Write audio data to file.

        :param recording_data: The audio data to write.
        :param detections: The detection data associated with the audio.
        :param detection_timestamp: The timestamp of the detection.
        :param input_index: The index of the input.
        """
        self.audio_writer.write_audio(
            recording_data, detections, detection_timestamp, input_index
        )
        logging.debug("Audio written from DetectionsWriter.")

    def stop(self):
        """
        Stop the DetectionsWriter thread.
        """
        self._stop_event.set()
        logging.debug("Waiting for DetectionsWriter thread to finish.")
        self._writer_thread.join()
        logging.debug("DetectionsWriter thread stopped.")
