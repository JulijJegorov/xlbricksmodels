"""
    Author: julij
    Date: 04/05/2025
    Description: Helper functions for QuantLib
"""

import numpy as np
import QuantLib as ql
from datetime import datetime
import QuantSpace.libs.qlutils as qlu


def year_fraction(day_counter: ql.DayCounter, start_date: datetime, end_date: datetime):
    """
        Calculate the year fraction between two dates using a specified day counter.
    :param day_counter: day counter type (e.g. 'ACT/360', '30/360', etc.)
    :param start_date: start date
    :param end_date: end date
    :return: year fraction
    """
    day_counter = qlu.ql_day_counter(day_counter)
    start_date = qlu.py_to_ql_date(start_date)
    end_date = qlu.py_to_ql_date(end_date)
    return day_counter.yearFraction(start_date, end_date)


def schedule(start_date: datetime, end_date: datetime, tenor: str, calendar: str, bdc: str, end_date_bdc: str, date_generation_rule: str, end_of_month: bool):
    """
        Create a schedule of dates between two dates with specified tenor, calendar, business day convention, and date generation rule.
    :param start_date: start date
    :param end_date: end date
    :param tenor: tenor (e.g. '1M', '3M', '6M', '1Y')
    :param calendar: calendar type (e.g. 'TARGET', 'US', etc.)
    :param bdc: business day convention (e.g. 'Following', 'Preceding', etc.)
    :param end_date_bdc: end date business day convention (e.g. 'Following', 'Preceding', etc.)
    :param date_generation_rule: date generation rule (e.g. 'Backward', 'Forward', 'Zero', etc.)
    :param end_of_month: end of month flag (True or False)
    :return: schedule of dates
    """
    start_date = qlu.py_to_ql_date(start_date)
    end_date = qlu.py_to_ql_date(end_date)
    tenor = qlu.ql_period(tenor)
    calendar = qlu.ql_calendar(calendar)
    bdc = qlu.ql_weekday_correction(bdc)
    end_date_bdc = qlu.ql_weekday_correction(end_date_bdc)
    date_generation_rule = qlu.ql_date_generation(date_generation_rule)
    ql_schedule = ql.Schedule(start_date, end_date, tenor, calendar, bdc, end_date_bdc, date_generation_rule, end_of_month)
    return np.array([datetime(x.year(), x.month(), x.dayOfMonth()) for x in ql_schedule]).reshape(-1, 1)



