# sndid/analyzerwrapper.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import logging
import io
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from typing import Any, Dict, Union
from pydantic import BaseModel, Field, validator
from .jack_lazy_loader import jack_lazy_load


class Config(BaseModel):
    """
    Configuration for the AnalyzerWrapper.
    """

    sample_rate: int = Field(..., gt=0)
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    min_confidence: float = Field(..., ge=0, le=1)

    @validator("sample_rate", "min_confidence")
    def not_negative(cls, v):
        """
        Validator to ensure the value is not negative.

        :param v: The value to validate
        :return: The validated value
        :raises ValueError: If the value is negative
        """
        if v < 0:
            raise ValueError("Value must be non-negative")
        return v


class AnalyzerWrapper:
    """
    AnalyzerWrapper class to interface with the BirdNet library.
    """

    def __init__(self, config: Dict[str, Union[int, float]]) -> None:
        """
        Initialize the AnalyzerWrapper instance.

        :param config: Configuration for the AnalyzerWrapper
        """
        self.config = Config(**config)
        self.Analyzer = jack_lazy_load("birdnetlib.analyzer").Analyzer
        self.RecordingBuffer = jack_lazy_load("birdnetlib").RecordingBuffer
        self.analyzer = self.Analyzer()

    def analyze(self, input_index: int, segment: Any) -> None:
        """
        Analyze an audio segment.

        :param input_index: Index of the input audio segment
        :param segment: Audio segment to analyze
        :return: None
        """
        logging.debug(f"Running analyzer for input {input_index + 1}")
        with io.StringIO() as f, redirect_stdout(f), redirect_stderr(f):
            recording_timestamp = datetime.now()
            logging.debug(
                f"Creating RecordingBuffer instance for input {input_index + 1}"
            )
            recording = self.RecordingBuffer(
                self.analyzer,
                segment,
                self.config.sample_rate,
                lat=self.config.lat,
                lon=self.config.lon,
                date=recording_timestamp,
                min_conf=self.config.min_confidence,
            )
            logging.debug(f"Analyzing RecordingBuffer for input {input_index + 1}")
            recording.analyze()

        if recording.detections:
            logging.info(
                f"Detections for input {input_index + 1}: {recording.detections}"
            )
        return recording, recording_timestamp
