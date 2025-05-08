"""
    Author: julij
    Date: 04/05/2025
    Description: Volatility models for QuantLib
"""

import numpy as np
import QuantLib as ql
from typing import List
from datetime import datetime
import QuantSpace.libs.qlutils as qlu


def black_constant_vol(evaluation_date: datetime, calendar: str, volatility: float, day_counter: str):
    """
        Create a Black constant volatility object.
    :param evaluation_date: Evaluation date
    :param calendar: Calendar name
    :param volatility: Volatility value
    :param day_counter: Day counter name
    :return: Black constant volatility object
    """
    evaluation_date = qlu.py_to_ql_date(evaluation_date)
    day_counter = qlu.ql_day_counter(day_counter)
    calendar = qlu.ql_calendar(calendar)
    volatility = ql.BlackConstantVol(evaluation_date, calendar, ql.QuoteHandle(ql.SimpleQuote(volatility)), day_counter)
    return volatility


def black_variance_surface(evaluation_date: datetime, calendar: str, expirations: List[datetime], strike_pries: List[float], volatility_matrix: np.ndarray, day_counter: str):
    """
        Create a Black variance surface object.
    :param evaluation_date: Evaluation date
    :param calendar: Calendar name
    :param expirations: List of expiration dates
    :param strike_pries: List of strike prices
    :param volatility_matrix: 2D numpy array of volatilities
    :param day_counter: Day counter name
    :return: Black variance surface object
    """
    evaluation_date = qlu.py_to_ql_date(evaluation_date)
    calendar = qlu.ql_calendar(calendar)
    expirations = [qlu.py_to_ql_date(date) for date in expirations]
    day_counter = qlu.ql_day_counter(day_counter)
    ql_volatility_matrix = ql.Matrix(len(strike_pries), len(expirations))
    for row in range(volatility_matrix.shape[0]):
        for col in range(volatility_matrix.shape[1]):
            ql_volatility_matrix[row][col] = volatility_matrix[row, col]
    surface = ql.BlackVarianceSurface(evaluation_date, calendar,  expirations, strike_pries, ql_volatility_matrix, day_counter)
    return surface


def volatility_from_surface(surface: ql.BlackVarianceSurface, expiry_date: datetime, strike_price: float):
    """
        Get the volatility from the Black variance surface.
    :param surface: Variance surface object
    :param expiry_date: Expiration date
    :param strike_price: Strike price
    :return:
    """
    expiration = qlu.py_to_ql_date(expiry_date)
    volatility = surface.blackVol(expiration, strike_price)
    return volatility
