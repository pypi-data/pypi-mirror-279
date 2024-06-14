# sndid/audiodetectionwriter.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import logging
import queue
import threading
from typing import Any, Tuple
from .detectionswriter import DetectionsWriter


class AudioDetectionWriter:
    """
    Class for writing audio detections to file.

    This class writes audio detections to file using a separate writer thread.
    It uses a queue to buffer the detection data and writes the data to file
    in the background. This allows for efficient handling of detection data
    while avoiding blocking the main thread.

    Attributes:
        detections_writer (DetectionsWriter): The detections writer object
            that handles writing the detection data to file.
        detection_queue (queue.Queue): The queue used to buffer the detection
            data.
        _stop_event (threading.Event): The stop event used to signal the
            writer thread to stop.
    """

    def __init__(
        self, detections_file: str, detections_dir: str, max_queue_size: int = 1000
    ):
        """
        Initialize the AudioDetectionWriter object.

        Args:
            detections_file (str): The file to write the detection data to.
            detections_dir (str): The directory where the detection file is
                located.
            max_queue_size (int, optional): The maximum size of the detection
                queue. Defaults to 1000.
        """

        logging.debug("Initialize AudioDetectionWriter")
        self.detections_writer = DetectionsWriter(detections_file, detections_dir)
        self.detection_queue = queue.Queue(maxsize=max_queue_size)
        self._stop_event = threading.Event()
        self._start_writer_thread()

    def __del__(self):
        """
        Stop and clean up the AudioDetectionWriter object.
        """
        self.stop()

    def write_detections(
        self,
        recording_data: Any,
        detections: Any,
        detection_timestamp: float,
        input_index: int,
    ):
        """
        Write detection data to the detection queue.

        This method writes the detection data to the detection queue, which
        is then processed by the writer thread.

        Args:
            recording_data (Any): The recording data associated with the
                detection.
            detections (Any): The detection data.
            detection_timestamp (float): The timestamp of the detection.
            input_index (int): The index of the input associated with the
                detection.
        """
        logging.debug("Putting data onto the queue")
        try:
            self.detection_queue.put_nowait(
                (recording_data, detections, detection_timestamp, input_index)
            )
        except queue.Full:
            logging.warning("Detection queue is full, skipping detection")

    def _write_detections_loop(self):
        """
        Write detection data from the queue to file.

        This method runs in the writer thread and continuously processes
        detection data from the queue, writing it to file.
        """
        while not self._stop_event.is_set():
            try:
                data = self.detection_queue.get(timeout=1)
                logging.debug("Got data from the queue")
                recording_data, detections, detection_timestamp, input_index = data
                self.detections_writer.write_detections(
                    detections, detection_timestamp, input_index
                )
                self.detections_writer.write_audio(
                    recording_data, detections, detection_timestamp, input_index
                )
                logging.debug("Wrote data to file")
            except queue.Empty:
                continue

    def _start_writer_thread(self):
        """
        Start the writer thread.

        This method starts the writer thread, which runs the
        _write_detections_loop method.
        """
        logging.basicConfig(level=logging.DEBUG)
        self._writer_thread = threading.Thread(
            target=self._write_detections_loop, daemon=True
        )
        self._writer_thread.start()

    def stop(self):
        """
        Stop the AudioDetectionWriter object.

        This method stops the writer thread and cleans up the object.
        """
        self._stop_event.set()
        self._writer_thread.join()
        self.detections_writer.flush()
        logging.debug("Writer stopped")

    def flush(self):
        """
        Flush the detection data to file.

        This method flushes any remaining detection data in the queue to file.
        """
        self.detections_writer.flush()
