"""This module contains types and validators meant to be used with Pydantic."""

from datetime import datetime
from decimal import Decimal
from functools import partial
from typing import Annotated
from zoneinfo import ZoneInfo

from pydantic import AfterValidator, BeforeValidator, Field, TypeAdapter


def timestamp_from_dt(dt: datetime) -> float:
    return dt.timestamp()


def s_to_ms(seconds: float) -> float:
    return seconds * 1000


def assert_str(s: str) -> str:
    """Validate string."""
    if not isinstance(s, str):
        raise ValueError(f"Invalid string: {s}")  # noqa: TRY004
    return s


def str_to_zoneinfo(tz: str) -> ZoneInfo:
    """Validate and convert to ZoneInfo."""
    try:
        return ZoneInfo(tz)
    except Exception as e:
        raise ValueError(f"Invalid timezone string: {tz}") from e


def to_decimal(value: str | float | int | Decimal, decimal_places: int, round_digits: int | None = None) -> Decimal:
    """Converts the given value to a decimal value.

    Args:
        value: The value to convert.
        decimal_places: The number of digits after the decimal point.
        round_digits: Only use this if you want trailing zeros. For example, if you want the input rounded to the
            nearest integer, but represented as a decimal with a single 0 after the decimal point, set round_digits to
            0 and decimal_places to 1.

    Example:
        >>> to_decimal(3.14159265358979, 2)
        3.12

        >>> to_decimal(3.14159265358979, 2, round_digits=0)
        3.00

    """
    if isinstance(value, str):
        value = Decimal(value)
    value = round(value, round_digits if round_digits is not None else decimal_places)
    return Decimal(f"{value:.{decimal_places}f}")


"""Convert to Decimal with a whole number followed by a decimal point and a single 0."""
WholeNumberDecimal = Annotated[
    Decimal,
    BeforeValidator(partial(to_decimal, decimal_places=1, round_digits=0)),
]

"""Convert to Decimal with 1 decimal place."""
Decimal1 = Annotated[
    Decimal,
    BeforeValidator(partial(to_decimal, decimal_places=1)),
]

"""Convert to Decimal with 2 decimal places."""
Decimal2 = Annotated[
    Decimal,
    BeforeValidator(partial(to_decimal, decimal_places=2)),
]

"""Validate string and convert to lowercase."""
LowercaseStr = Annotated[str, Field(validate_default=True), AfterValidator(str.lower)]

"""Validate string and convert to uppercase."""
UppercaseStr = Annotated[str, Field(validate_default=True), AfterValidator(str.upper)]

"""
Validate and convert to timestamp (seconds).

The input could be a datetime object, a string, a float, an int, or anything Pydantic is able to parse as a datetime.
"""
IntTimestampS = Annotated[
    datetime,
    Field(validate_default=True),
    AfterValidator(timestamp_from_dt),
    AfterValidator(int),
]

IntTimestampMS = Annotated[
    datetime,
    Field(validate_default=True),
    AfterValidator(timestamp_from_dt),
    AfterValidator(s_to_ms),
    AfterValidator(int),
]

FloatTimestampS = Annotated[datetime, Field(validate_default=True), AfterValidator(timestamp_from_dt)]

FloatTimestampMS = Annotated[
    datetime,
    Field(validate_default=True),
    AfterValidator(timestamp_from_dt),
    AfterValidator(s_to_ms),
]

"""Validate a datetime string by converting to datetime and back to string."""
StrTimestampISO = Annotated[
    str,
    Field(validate_default=True),
    BeforeValidator(assert_str),
    AfterValidator(lambda s: TypeAdapter(datetime).validate_python(s)),
    AfterValidator(lambda dt: dt.isoformat(sep=" ", timespec="seconds")),
]

"""Validate and convert to ZoneInfo."""
TimeZone = Annotated[ZoneInfo, Field(validate_default=True), BeforeValidator(str_to_zoneinfo)]

"""Validate timezone string."""
TimeZoneString = Annotated[str, Field(validate_default=True), AfterValidator(str_to_zoneinfo), AfterValidator(str)]
