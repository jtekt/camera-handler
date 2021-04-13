from pydantic import BaseModel
from typing import Optional


class Configuration(BaseModel):
    brightness: Optional[int] = None
    contrast: Optional[int] = None
    saturation: Optional[int] = None
    hue: Optional[int] = None
    white_balance_temperature_auto: Optional[int] = None
    gamma: Optional[int] = None
    gain: Optional[int] = None
    power_line_frequency: Optional[int] = None
    white_balance_temperature: Optional[int] = None
    sharpness: Optional[int] = None
    backlight_compensation: Optional[int] = None
    exposure_auto: Optional[int] = None
    exposure_absolute: Optional[int] = None
    exposure_auto_priority: Optional[int] = None
