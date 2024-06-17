from decimal import Decimal

import dateparser
import math
import pytz

from datetime import datetime


def date_to_milliseconds(date_str: str) -> int:
    """Convert UTC date to milliseconds

    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    See dateparse docs for formats https://dateparser.readthedocs.io/en/latest/

    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    """
    # get epoch value in UTC
    epoch: datetime = datetime.fromtimestamp(0, tz=pytz.utc)
    # parse our date string
    d: datetime = dateparser.parse(date_str, settings={"TIMEZONE": "UTC"})
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


def round_step_size(quantity: float | Decimal, step_size: float | Decimal) -> float:
    """Rounds a given quantity to a specific step size

    :param quantity: required
    :param step_size: required

    :return: decimal
    """
    precision: int = int(round(-math.log(step_size, 10), 0))
    return float(round(quantity, precision))


def convert_ts_str(ts_str) -> int | None:
    if ts_str is None:
        return ts_str
    if isinstance(ts_str, int):
        return ts_str
    return date_to_milliseconds(ts_str)
