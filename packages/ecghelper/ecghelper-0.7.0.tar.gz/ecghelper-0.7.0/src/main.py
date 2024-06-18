import base64
import lxml.etree as ET
import os
import random
from pathlib import Path
from zlib import crc32

import boto3

from ecghelper.record import record_from_xml


def check_crc(xml_path: Path):
    root = ET.parse(xml_path).getroot()
    waveform = None
    for waveform in root.iter("Waveform"):
        waveform_type = waveform.find("WaveformType").text
        if waveform_type != "Rhythm":
            continue

        for lead in waveform.iter("LeadData"):
            lead_name = lead.find("LeadID").text
            # verify data matches the CRC32
            lead_data = lead.find("WaveFormData").text
            lead_crc32 = int(lead.find("LeadDataCRC32").text)
            decoded = base64.b64decode(lead_data)
            computed = crc32(decoded)
            if lead_crc32 != computed:
                print(
                    f"CRC32 mismatch in {lead_name}; expected {lead_crc32} and received {computed}"
                )
            else:
                print(f"CRC32 match in {lead_name}")


def download_random_sharp(num: int, d: str):
    bucket = "s3-sharp-bucket"
    prefix = "MUSE/2.0.4"

    s3 = boto3.client("s3")

    for _ in range(num):
        hex_prefix = str(hex(int(random.random() * 65536)))[2:]
        objs = s3.list_objects_v2(Bucket=bucket, Prefix=f"{prefix}/{hex_prefix}")
        obj = random.choice(objs["Contents"])
        key = obj["Key"]
        s3.download_file(Bucket=bucket, Key=key, Filename=d + "/" + key.split("/")[-1])


if __name__ == "__main__":
    d = "/Users/jasonma/Desktop/GE_MUSE"
    for f in os.listdir(d):
        if f.endswith(".xml"):
            print(f"Checking {f}")
            # check_crc(Path(d) / f)
            r = record_from_xml(Path(d) / f)
            print("\n\n\n")
