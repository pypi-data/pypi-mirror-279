import numpy as np
import pytest

from ecghelper.waveform import WaveformRecord

# load_wfdb(), write_wfdb() tests
@pytest.mark.parametrize("filename", ["A0001"])
def test_speed_load_wfdb(filename, cpsc_2018_path, benchmark):
    signal = benchmark(WaveformRecord.from_wfdb, cpsc_2018_path / filename)
    assert signal is not None

@pytest.mark.parametrize("filename", ["A0001"])
def test_speed_write_wfdb(filename, cpsc_2018_path, benchmark, tmp_path):
    signal = WaveformRecord.from_wfdb(cpsc_2018_path / filename)
    benchmark(signal.to_wfdb, tmp_path / filename)
    assert signal is not None

@pytest.mark.parametrize("filename", ["A0001.edf"])
def test_speed_load_edf(filename, cpsc_2018_path, benchmark):
    signal = benchmark(WaveformRecord.from_edf, cpsc_2018_path / filename)
    assert signal is not None

@pytest.mark.parametrize("filename", ["A0001.edf"])
def test_speed_write_edf(filename, cpsc_2018_path, benchmark, tmp_path):
    signal = WaveformRecord.from_edf(cpsc_2018_path / filename)
    signal.data = np.around(signal.data, 8)
    benchmark(signal.to_edf, tmp_path / filename)
    assert signal is not None

@pytest.mark.parametrize("filename", ["A0001.xml"])
def test_speed_load_xml(filename, cpsc_2018_path, benchmark):
    signal = benchmark(WaveformRecord.from_xml, cpsc_2018_path / filename)
    assert signal is not None

@pytest.mark.parametrize("filename", ["A0001.xml"])
def test_speed_write_xml(filename, cpsc_2018_path, benchmark, tmp_path):
    signal = WaveformRecord.from_xml(cpsc_2018_path / filename)
    benchmark(signal.to_xml, tmp_path / filename)
    assert signal is not None
