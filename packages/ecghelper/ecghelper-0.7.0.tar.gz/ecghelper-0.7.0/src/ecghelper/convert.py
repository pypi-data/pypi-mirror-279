"""Utilities to support converting from one format to another."""
from pathlib import Path
from typing import Union

from ecghelper.waveform import WaveformRecord


def convert(
    source_record: Union[str, Path],
    source_format: str,
    target_record: Union[str, Path],
    target_format: str,
):
    """Convert from one format to another."""
    # Load the source data based on the format
    if source_format == "xml":
        record = WaveformRecord.from_xml(source_record)
    elif source_format == "csv":
        record = WaveformRecord.from_csv(source_record)
    elif source_format == "wfdb":
        record = WaveformRecord.from_wfdb(source_record)
    elif source_format == "edf":
        record = WaveformRecord.from_edf(source_record)
    else:
        raise ValueError("Unknown source format: {}".format(source_format))

    # get fcn to write out to target format
    write_fcn = record.write_methods[target_format]

    # if target_record is a string, treat it as a file path
    if isinstance(target_record, str):
        target_record = Path(target_record)
    write_fcn(target_record)
