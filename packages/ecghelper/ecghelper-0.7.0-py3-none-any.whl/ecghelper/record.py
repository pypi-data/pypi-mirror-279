import lxml.etree as ET
from datetime import datetime
from dateutil.parser import parse
from pathlib import Path

from dandelion_data_schema.record import (
    ModalityType,
    Record,
    SexEnum,
    RaceEthnicityEnum,
    WaveformStudy,
)

from .waveform import WaveformMetadata, WaveformRecord


def parse_sex(metadata: WaveformMetadata):
    if metadata.sex is None or metadata.sex == "OMITTED":
        return None
    elif metadata.sex.lower() == "female":
        return SexEnum.female
    elif metadata.sex.lower() == "male":
        return SexEnum.male
    else:
        return SexEnum.other


def parse_race(metadata: WaveformMetadata):
    if metadata.race is None or metadata.race == "OMITTED":
        return None
    else:
        return RaceEthnicityEnum(metadata.race)


def parse_age_from_dob(root):
    dob = root.find("PatientDemographics/DateofBirth")
    if dob is None:
        return None
    acquisition_date = root.find("TestDemographics/AcquisitionDate")
    if acquisition_date is None:
        return None
    dob = parse(dob.text)
    acquisition_date = parse(acquisition_date.text)
    age = int((acquisition_date - dob).days / 365.2425)
    return age


def parse_age(metadata: WaveformMetadata):
    if metadata.age is None or metadata.age == "OMITTED":
        return None
    else:
        return metadata.age


def parse_studytime(root: ET.Element):
    test_demographics = root.find("TestDemographics")
    time = test_demographics.find("AcquisitionTime").text
    date = test_demographics.find("AcquisitionDate").text
    try:
        return datetime.strptime(f"{date} {time}", "%m-%d-%Y %H:%M:%S")
    except Exception:
        return parse(date)


def record_from_xml(xml_path: Path) -> Record:
    waveform = WaveformRecord.from_xml(xml_path)
    metadata = WaveformMetadata.from_xml(xml_path)

    print(f"Parsing {xml_path}")
    root = ET.parse(xml_path).getroot()

    studytime = parse_studytime(root)
    age = parse_age(metadata)
    if age is None:
        age = parse_age_from_dob(root)

    return Record(
        record_name=str(xml_path),
        age_at_study_time=age,
        sex=parse_sex(metadata),
        race_ethnicity=parse_race(metadata),
        modality_type=ModalityType.waveform,
        modality_data=WaveformStudy(
            studytime=studytime,
            sampling_frequency=waveform.sampling_frequency,
            signal_names=waveform.columns,
            waveform=waveform.data,
        ),
    )
