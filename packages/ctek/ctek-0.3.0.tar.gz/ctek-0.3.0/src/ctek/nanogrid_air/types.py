from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class BaseDataClass:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def __str__(self) -> str:
        return f"{self.to_dict()}"


@dataclass
class DeviceInfo(BaseDataClass):
    serial: str
    firmware: str
    mac: str


@dataclass
class ChargeboxInfo(BaseDataClass):
    identity: str
    serial: str
    firmware: str
    endpoint: str
    port: int
    state: str
    pinned: bool


@dataclass
class MeterInfo(BaseDataClass):
    vendor: str
    type: str
    id: str


@dataclass
class OTAInfo(BaseDataClass):
    status: int
    version: str
    progress: int


@dataclass
class DeviceStatus(BaseDataClass):
    device_info: DeviceInfo
    chargebox_info: ChargeboxInfo
    meter_info: MeterInfo
    ota_info: OTAInfo


@dataclass
class MeterData(BaseDataClass):
    active_power_in: float
    active_power_out: float
    current_L1: float
    current_L2: float
    current_L3: float
    voltage_L1: float
    voltage_L2: float
    voltage_L3: float
    total_energy_active_import: int
    total_energy_active_export: int


@dataclass
class MeterRawData(BaseDataClass):
    result: str
    cpu_time_ms: int
    length: int
    data: str


@dataclass
class EVSEInfo(BaseDataClass):
    id: int
    state: int
    current: list[float]


@dataclass
class EVSEData(BaseDataClass):
    cb_id: str
    connection_status: str
    evse: list[EVSEInfo] = field(default_factory=list)
