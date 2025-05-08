"""
    Author: julij
    Date: 04/05/2025
    Description: Yield curve models for QuantLib
"""

import numpy as np
import QuantLib as ql
from typing import List
from datetime import datetime
import QuantSpace.libs.qlutils as qlu


def forward_curve(dates: List[datetime], rates: List[datetime], day_counter: str, calendar: str):
    """
        Create a forward curve object.
    :param dates: Dates for the forward curve
    :param rates: Rates for the forward curve
    :param day_counter: Day counter name
    :param calendar: calendar name
    :return: Forward curve object
    """
    dates = [qlu.py_to_ql_date(date) for date in dates]
    day_counter = qlu.ql_day_counter(day_counter)
    calendar = qlu.ql_calendar(calendar)
    yield_curve = ql.ForwardCurve(dates, rates, day_counter, calendar)
    return yield_curve


def flat_forward(date: datetime, rate: float, day_counter: str, compounding: str, frequency: str):
    """
        Create a flat forward yield curve object.
    :param date: Date for the flat forward curve
    :param rate: Rate for the flat forward curve
    :param day_counter: Day counter name
    :param compounding: Compounding method
    :param frequency: Frequency of the compounding
    :return: Flat forward yield curve object
    """
    date = qlu.py_to_ql_date(date)
    day_counter = qlu.ql_day_counter(day_counter)
    compounding = qlu.ql_compounding(compounding)
    frequency = qlu.ql_frequency(frequency)
    return ql.FlatForward(date, rate, day_counter, compounding, frequency)


def zero_rates(yield_curve, dates, day_counter, compounding):
    """
        Get the zero rates from the yield curve.
    :param yield_curve: Yield curve object
    :param dates: Dates for the zero rates
    :param day_counter: Day counter name
    :param compounding: Compounding method
    :return: Array of zero rates
    """
    dates = [qlu.py_to_ql_date(date) for date in dates]
    day_counter = qlu.ql_day_counter(day_counter)
    compounding = qlu.ql_compounding(compounding)
    return np.array([yield_curve.zeroRate(date, day_counter, compounding).rate() for date in dates])
