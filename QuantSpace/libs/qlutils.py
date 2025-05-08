"""
    Author: julij
    Date: 04/05/2025
    Description: Utility functions for QuantLib
"""

import QuantLib as ql
from datetime import datetime

DAY_COUNTERS = {
    'SIMPLE': ql.SimpleDayCounter(),
    '30/360': ql.Thirty360(),
    'ACT/360': ql.Actual360(),
    'ACT/365Fixed': ql.Actual365Fixed(),
    'ACT/365FixedCAD': ql.Actual365Fixed(ql.Actual365Fixed.Canadian),
    'ACT/365FixedNoLeap': ql.Actual365Fixed(ql.Actual365Fixed.NoLeap),
    'ACT/ACT': ql.ActualActual(),
    'BUS/252': ql.Business252()
}

CALENDARS = {
    'UK': ql.UnitedKingdom(),
    'GR': ql.Germany(),
    'IT': ql.Italy(),
    'US': ql.UnitedStates(),
}


WEEKDAY_CORRECTION = {
    'UNADJUSTED': ql.Unadjusted,
    'FOLLOWING': ql.Following,
    'MOD_FOLLOWING': ql.ModifiedFollowing,
    'PRECEDING': ql.Preceding,
    'MOD_PRECEDING': ql.ModifiedPreceding
}

DATE_GENERATION = {
    'FORWARD': ql.DateGeneration.Forward,
    'BACKWARD': ql.DateGeneration.Backward,
    'ZERO': ql.DateGeneration.Zero,
    'THIRD_WEDNESDAY': ql.DateGeneration.ThirdWednesday,
    'TWENTIETH': ql.DateGeneration.Twentieth,
    'TWENTIETH_IMM': ql.DateGeneration.TwentiethIMM,
    'CDS': ql.DateGeneration.CDS
}

COMPOUNDING = {
    'SIMPLE': ql.Simple,
    'COMPOUNDED': ql.Compounded,
    'CONTINUOUS': ql.Continuous
}

FREQUENCIES = {
    'NOFREQUENCY': ql.NoFrequency,
    'ONCE':	ql.Once,
    'ANNUAL': ql.Annual,
    'SEMIANNUAL': ql.Semiannual,
    'EVERYFOURTHMONTH':	ql.EveryFourthMonth,
    'QUARTERLY': ql.Quarterly,
    'BIMONTHLY': ql.Bimonthly,
    'MONTHLY': ql.Monthly,
    'EVERYFOURTHWEEK': ql.EveryFourthWeek,
    'BIWEEKLY': ql.Biweekly,
    'WEEKLY': ql.Weekly,
    'DAILY': ql.Daily
}

DATE_GENERATION = {
    'BACKWARD': ql.DateGeneration.Backward,
    'FORWARD': ql.DateGeneration.Forward,
    'ZERO': ql.DateGeneration.Zero,
    'THIRD_WEDNESDAY': ql.DateGeneration.ThirdWednesday,
    'TWENTIETH': ql.DateGeneration.Twentieth,
    'TWENTIETH_IMM': ql.DateGeneration.TwentiethIMM,
    'CDS': ql.DateGeneration.CDS,
}


def ql_date_generation(rule: str):
    """
        Convert a string to a QuantLib date generation rule.
    :param rule: date generation rule as a string
    :return: QuantLib date generation rule
    """
    return DATE_GENERATION[rule.upper()]


def ql_weekday_correction(correction: str):
    """
        Convert a string to a QuantLib weekday correction rule.
    :param correction: weekday correction rule as a string
    :return: QuantLib weekday correction rule
    """
    return WEEKDAY_CORRECTION[correction.upper()]


def ql_calendar(calendar: str):
    """
        Convert a string to a QuantLib calendar.
    :param calendar: calendar name as a string
    :return: QuantLib calendar
    """
    return CALENDARS[calendar.upper()]


def ql_day_counter(day_counter: str):
    """
        Convert a string to a QuantLib day counter.
    :param day_counter: day counter name as a string
    :return: QuantLib day counter
    """
    return DAY_COUNTERS[day_counter.upper()]


def ql_period(period: str):
    """
        Convert a string to a QuantLib period.
    :param period: period as a string (e.g. '1Y', '6M', '3D')
    :return: QuantLib period
    """
    return ql.Period(period)


def ql_compounding(compounding: str):
    """
        Convert a string to a QuantLib compounding method.
    :param compounding: compounding method as a string
    :return: QuantLib compounding method
    """
    return COMPOUNDING[compounding.upper()]


def ql_frequency(frequency):
    """
        Convert a string to a QuantLib frequency.
    :param frequency: frequency as a string
    :return: QuantLib frequency
    """
    return FREQUENCIES[frequency.upper()]


def ql_date_generation(date_generation: str):
    """
        Convert a string to a QuantLib date generation rule.
    :param date_generation: date generation rule as a string
    :return: QuantLib date generation rule
    """
    return DATE_GENERATION[date_generation.upper()]


def py_to_ql_date(date: datetime):
    """
        Convert a Python datetime object to a QuantLib date.
    :param date: datetime object
    :return: QuantLib date
    """
    return ql.Date(date.day, date.month, date.year)


def ql_to_py_date(date: ql.Date):
    """
        Convert a QuantLib date to a Python datetime object.
    :param date: QuantLib date
    :return: datetime object
    """
    return datetime(date.year(), date.month(), date.dayOfMonth())
