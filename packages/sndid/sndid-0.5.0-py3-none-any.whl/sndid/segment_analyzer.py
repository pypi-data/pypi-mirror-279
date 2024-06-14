# sndid/segment_analyzer.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import threading
import logging


class SegmentAnalyzer(threading.Thread):
    """SegmentAnalyzer is a class that analyzes a given segment of data and returns
    any detections found within that segment. It does this by using an analyzer
    wrapper to analyze the segment and return any detections.
    """

    def __init__(self, analyzer_wrapper):
        """Initializes a new instance of the SegmentAnalyzer class with the given
        analyzer wrapper.

        Args:
            analyzer_wrapper (object): The analyzer wrapper to use for analyzing
            segments of data.
        """
        logging.debug("Initialize SegmentAnalyzer")
        self.analyzer_wrapper = analyzer_wrapper

    def analyze(self, input_index, segment):
        """Analyzes the given segment of data and returns any detections found within
        that segment.

        Args:
            input_index (int): The index of the input data being analyzed.
            segment (object): The segment of data to analyze.

        Returns:
            tuple: A tuple containing the analyzed segment, any detections found,
            and the timestamp of the detection. If no detections were found, this
            method returns None.
        """
        logging.debug(f"SegmentAnalyzer Analyzing segment for input {input_index}")
        recording, detection_timestamp = self.analyzer_wrapper.analyze(
            input_index, segment
        )
        if recording.detections:
            logging.debug(
                f"SegmentAnalyzer detections found in segment for input {input_index}: {recording.detections}"
            )
            return segment, recording.detections, detection_timestamp
        return None
