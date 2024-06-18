from dataclasses import dataclass
from .af import AlternativeFrequencyEntryDecoded

@dataclass
class Group:
    """This is a basic group function to store the blocks"""
    a:int
    b:int
    c:int
    d:int
    is_version_b: bool
    def to_list(self):
        return [self.a, self.b, self.c, self.d]
    def __iter__(self):
        return self.to_list()

@dataclass
class GroupIdentifier:
    group_number: int
    group_version: bool

@dataclass
class Details:
    details=""

@dataclass
class PSDetails(Details):
    segment: int
    di_stereo:bool
    di_artificial_head:bool
    di_compressed:bool
    di_dpty:bool
    ms: bool
    ta: bool
    text: str
    af: AlternativeFrequencyEntryDecoded
    details="PS"

@dataclass
class FastSwitchingInformation(Details):
    segment: int
    di_stereo:bool
    di_artificial_head:bool
    di_compressed:bool
    di_dpty:bool
    ms: bool
    ta: bool
    details="FSI"

@dataclass
class RTDetails(Details):
    segment: int
    ab: bool
    text: str
    details="RT"

@dataclass
class LongPSDetails(Details):
    segment: int
    text: str
    details="LPS"

@dataclass
class PTYNDetails(Details):
    segment: int
    ab: bool
    text: str
    details="PTYN"

@dataclass
class PINSLCetails(Details):
    data:int
    is_lic:bool
    is_broadcaster_data:bool
    variant_code: int
    pin_day: int
    pin_hour: int
    pin_minute: int
    details="PINSLC"

@dataclass
class CTDetails(Details):
    mjd: int
    hour: int
    minute: int
    time_sense: bool
    local_offset: int
    details="CT"

@dataclass
class TDCDetails(Details):
    channel: int
    data: list[int]
    details="TDC"

@dataclass
class InHouseDetails(Details):
    data: list[int]
    details="IH"

@dataclass
class ODADetails(Details):
    data: list[int]
    details="ODA"

@dataclass
class ODAAidDetails(Details):
    oda_group: GroupIdentifier
    aid:int
    scb:int
    details="ODAAID"

@dataclass
class EONBDetails(Details):
    pi: int
    tp: bool
    ta: bool
    details="EONB"

@dataclass
class EONADetails(Details):
    pi: int
    tp: bool
    ta: bool
    ps_segment:int
    ps_text:str
    pty: int
    on_af: int
    variant_code:int
    details="EONA"

@dataclass
class DecodedGroup:
    raw_group: Group
    pi: int
    tp: bool
    pty: int
    group: GroupIdentifier
    details: Details