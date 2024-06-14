# sndid/textdetectionwriter.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import logging
import queue
import threading
from .textwriter import TextWriter


class TextDetectionWriter:
    """
    A class for writing text detections to a file.

    This class uses a separate thread to periodically check a queue for new
    text detections and write them to a file. This allows the main program to
    continue running without being blocked by the time-consuming process of
    writing detections to a file.

    Args:
     detections_file (str): The file to which text detections will be written.
     detections_dir (str): The directory in which the detections file is located.

    Attributes:
     text_writer (TextWriter): An instance of the TextWriter class, which handles
                              the actual writing of text detections to a file.
     detection_queue (queue.Queue): A queue for storing text detections waiting to
                                    be written to a file.
     _stop_event (threading.Event): An event that can be set to stop the writer
                                     thread.
     _writer_thread (threading.Thread): A thread for periodically checking the
                                         detection queue and writing detections
                                         to a file.
    """

    def __init__(self, detections_file, detections_dir):
        """
        Initialize the TextDetectionWriter object.

        This method initializes the TextDetectionWriter object by creating a
        TextWriter object to handle the actual writing of text detections to a
        file, creating a queue for storing text detections waiting to be written
        to a file, and starting a separate thread for periodically checking the
        queue and writing detections to a file.

        Args:
         detections_file (str): The file to which text detections will be written.
         detections_dir (str): The directory in which the detections file is located.
        """
        logging.debug("Initializing TextDetectionWriter")
        self.text_writer = TextWriter(detections_file)
        self.detection_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._writer_thread = threading.Thread(target=self._write_detections_loop)
        self._writer_thread.daemon = True
        self._writer_thread.start()
        logging.debug("TextDetectionWriter thread started")

    def write_detections(self, detections, detection_timestamp, input_index):
        """
        Write text detections to the queue.

        This method writes the given text detections to the detection queue,
        allowing them to be written to a file by the writer thread.

        Args:
         detections (list): A list of text detections, where each detection is a
                            dictionary with keys 'text', 'confidence', and
                            'bounding_box'.
         detection_timestamp (float): The timestamp associated with the text
                                      detections.
         input_index (int): The index of the input from which the text detections
                            were obtained.
        """
        self.detection_queue.put((detections, detection_timestamp, input_index))
        logging.debug(
            f"TextDetectionWriter detections written to queue: {len(detections)}"
        )

    def _write_detections_loop(self):
        """
        Periodically check the detection queue and write detections to a file.

        This method runs in a separate thread and periodically checks the
        detection queue for new text detections. If there are new detections in
        the queue, they are written to a file by the TextWriter object.
        """
        while not self._stop_event.is_set():
            try:
                detections, detection_timestamp, input_index = self.detection_queue.get(
                    timeout=1
                )
                logging.debug("TextDetectionWriter received detections from queue")
            except queue.Empty:
                continue
            self.text_writer.write_detections(
                detections, detection_timestamp, input_index
            )
            logging.debug(
                f"TextDetectionWriter detections written to file: {len(detections)}"
            )

    def stop(self):
        """
        Stop the writer thread and join it.

        This method sets the stop event, causing the writer thread to exit its
        loop, and then joins the thread to wait for it to finish.
        """
        logging.debug("Stopping TextDetectionWriter")
        self._stop_event.set()
        self._writer_thread.join()
