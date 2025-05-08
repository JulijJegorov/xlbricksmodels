"""
    Author: julij
    Date: 04/05/2025
    Description: Wrapper functions for QuantLib used by xlbricks
"""

import numpy as np
from typing import Any
import QuantSpace.libs.qlmisc as qlmisc
import QuantSpace.libs.qlyield as qlyield
import QuantSpace.libs.qloptions as qloptions
import QuantSpace.libs.qlvolsurface as qlvolsurface


class QuantSpaceContext(object):

    @staticmethod
    def comdty_vanilla_option(evaluation_date: np.ndarray, expiry_date: np.ndarray, forward_price: np.ndarray, strike_price: np.ndarray, option_type: np.ndarray, exercise_type: np.ndarray,
                              volatility: Any, yield_curve: Any, steps: np.ndarray = np.array([[100]])):
        """
            Calculate the price of a commodity vanilla option.
        :param evaluation_date:  Date of evaluation
        :param expiry_date: Date of expiry
        :param forward_price: Forward price of the underlying asset
        :param strike_price: Strike price of the option
        :param option_type: 'CALL' or 'PUT'
        :param exercise_type: 'EUROPEAN' or 'AMERICAN'
        :param steps: Number of steps for the binomial tree (only for American options)
        :param volatility: Volatility term structure
        :param yield_curve: Yield term structure
        :return: DataFrame with option price, delta, gamma, theta, vega, rho
        """
        return qloptions.comdty_vanilla_option(evaluation_date[0, 0], expiry_date[0, 0], forward_price[0, 0], strike_price[0, 0], option_type[0, 0], exercise_type[0, 0], steps[0, 0], volatility, yield_curve)

    @staticmethod
    def comdty_vanilla_option_delta(evaluation_date: np.ndarray, expiry_date: np.ndarray, forward_price: np.ndarray, delta: np.ndarray, option_type: np.ndarray, volatility: Any, yield_curve: Any):
        """
        Calculate the delta of a commodity vanilla option.
        :param evaluation_date: Date of evaluation
        :param expiry_date: Date of expiry
        :param forward_price: Forward price of the underlying asset
        :param delta: Delta of the option
        :param option_type: 'CALL' or 'PUT'
        :param volatility: Volatility term structure
        :param yield_curve: Yield term structure
        :return: DataFrame with option price, delta, gamma, theta, vega, rho, derived strike price
                and helper values like d1, risk-free rate, atm volatility, years_to_maturity
        """
        return qloptions.comdty_vanilla_option_delta(evaluation_date[0, 0], expiry_date[0, 0], forward_price[0, 0], delta[0, 0], option_type[0, 0], volatility, yield_curve)

    @staticmethod
    def comdty_vanilla_option_calendar_spread(evaluation_date: np.ndarray, expiry_date_long: np.ndarray, expiry_date_short: np.ndarray, forward_price: np.ndarray, strike_price: np.ndarray, option_type: np.ndarray,
                                              correlation: np.ndarray, volatility: Any, yield_curve: Any, paths: np.ndarray):
        """
            Calculate the price of a commodity vanilla option calendar spread.
        :param evaluation_date: Date of evaluation
        :param expiry_date_long: Date of long expiry
        :param expiry_date_short: Date of short expiry
        :param forward_price: Forward price of the underlying asset
        :param strike_price: Strike price of the option
        :param option_type: CALL or PUT
        :param correlation: Correlation between the two underlying assets
        :param volatility: Volatility term structure
        :param yield_curve: Yield term structure
        :param paths: Number of paths for Monte Carlo simulation
        :return: DataFrame with the price of vanilla calendar spread and helper values
        """
        return qloptions.comdty_vanilla_option_calendar_spread(evaluation_date[0, 0], expiry_date_long[0, 0], expiry_date_short[0, 0], forward_price[0, 0], strike_price[0, 0], option_type[0, 0], correlation[0, 0], volatility, yield_curve, paths[0, 0])

    @staticmethod
    def comdty_vanilla_option_spread(evaluation_date: np.ndarray, expiry_date: np.ndarray, forward_price: np.ndarray, strike_price_long: np.ndarray, strike_price_short: np.ndarray, option_type: np.ndarray, exercise_type: np.ndarray,
                                     volatility: Any, yield_curve: Any, steps: np.ndarray = np.array([[100]])):
        """
            Calculate the price of a commodity vanilla option spread.
        :param evaluation_date: Date of evaluation
        :param expiry_date: Date of expiry
        :param forward_price: Forward price of the underlying asset
        :param strike_price_long: Strike price of the long option
        :param strike_price_short: Strike price of the short option
        :param option_type: CALL or PUT
        :param exercise_type: EUROPEAN or AMERICAN
        :param steps:  Number of steps for the binomial tree (only for American options)
        :param volatility: Volatility term structure
        :param yield_curve: Yield term structure
        :return: DataFrame with option price, delta, gamma, theta, vega, rho for both options and the spread
        """
        return qloptions.comdty_vanilla_option_spread(evaluation_date[0, 0], expiry_date[0, 0], forward_price[0, 0], strike_price_long[0, 0], strike_price_short[0, 0], option_type[0, 0], exercise_type[0, 0], steps[0, 0], volatility, yield_curve)

    @staticmethod
    def comdty_vanilla_option_collar(evaluation_date: np.ndarray, expiry_date: np.ndarray, forward_price: np.ndarray, strike_price_call_short: np.ndarray, strike_price_put_long: np.ndarray, exercise_type: np.ndarray,
                                     volatility: Any, yield_curve: Any, steps: np.ndarray = np.array([[100]])):
        """
            Calculate the price of a commodity vanilla option collar.
        :param evaluation_date: Date of evaluation
        :param expiry_date: Expiry date
        :param forward_price: Forward price of the underlying asset
        :param strike_price_call_short: Strike price of a short call option
        :param strike_price_put_long: Strike price of a long put option
        :param exercise_type: EUROPEAN or AMERICAN
        :param steps: Number of steps for the binomial tree (only for American options)
        :param volatility: Volatility term structure
        :param yield_curve: Yield term structure
        :return: DataFrame with option price, delta, gamma, theta, vega, rho for both options and the collar
        """
        return qloptions.comdty_vanilla_option_collar(evaluation_date[0, 0], expiry_date[0, 0], forward_price[0, 0], strike_price_call_short[0, 0], strike_price_put_long[0, 0],  exercise_type[0, 0], steps[0, 0], volatility, yield_curve)

    @staticmethod
    def comdty_vanilla_option_butterfly(evaluation_date: np.ndarray, expiry_date: np.ndarray, forward_price: np.ndarray, strike_price_low_long: np.ndarray, strike_price_middle_short: np.ndarray, strike_price_high_long: np.ndarray, option_type: np.ndarray, exercise_type: np.ndarray,
                                        volatility: Any, yield_curve: Any, steps: np.ndarray = np.array([[100]])):
        """
            Calculate the price of a commodity vanilla option butterfly.
        :param evaluation_date: Date of evaluation
        :param expiry_date: Date of expiry
        :param forward_price: Forward price of the underlying asset
        :param strike_price_low_long: Strike price of the low long option
        :param strike_price_middle_short: Strike price of two short middle option
        :param strike_price_high_long: Strike price of the high long option
        :param option_type: CALL or PUT
        :param exercise_type: EUROPEAN or AMERICAN
        :param steps: Number of steps for the binomial tree (only for American options)
        :param volatility: Volatility term structure
        :param yield_curve: Yield term structure
        :return: DataFrame with option price, delta, gamma, theta, vega, rho for all three options and the butterfly spread
        """
        return qloptions.comdty_vanilla_option_butterfly(evaluation_date[0, 0], expiry_date[0, 0], forward_price[0, 0], strike_price_low_long[0, 0], strike_price_middle_short[0, 0], strike_price_high_long[0, 0], option_type[0, 0], exercise_type[0, 0], steps[0, 0], volatility, yield_curve)

    @staticmethod
    def black_constant_vol(evaluation_date: np.ndarray, volatility: np.ndarray, calendar: np.ndarray, day_counter: np.ndarray):
        """
            Calculate the Black constant volatility.
        :param evaluation_date: Evaluation date
        :param calendar: Calendar name
        :param volatility: Volatility value
        :param day_counter: Day counter name
        :return: Black constant volatility object
        """
        return qlvolsurface.black_constant_vol(evaluation_date[0, 0], calendar[0, 0], volatility[0, 0], day_counter[0, 0])

    @staticmethod
    def black_variance_surface(evaluation_date: np.ndarray, expirations: np.ndarray, strike_pries: np.ndarray, volatility_matrix: np.ndarray, day_counter: np.ndarray, calendar: np.ndarray,):
        """
            Create a Black variance surface.
        :param evaluation_date: Evaluation date
        :param calendar: Calendar name
        :param expirations: List of expiration dates
        :param strike_pries: List of strike prices
        :param volatility_matrix: 2D numpy array of volatilities
        :param day_counter: Day counter name
        :return: Black variance surface object
        """
        return qlvolsurface.black_variance_surface(evaluation_date[0, 0], calendar[0, 0], expirations.flatten().tolist(), strike_pries.flatten().tolist(), volatility_matrix, day_counter[0, 0])

    @staticmethod
    def volatility_from_surface(surface: np.ndarray, expiry_date: np.ndarray, strike_price: np.ndarray):
        """
            Calculate the volatility from a given surface.
        :param surface: Volatility surface
        :param expiry_date: Expiry date
        :param strike_price: Strike price
        :return: Volatility value"""
        return qlvolsurface.volatility_from_surface(surface, expiry_date[0, 0], strike_price[0, 0])

    @staticmethod
    def zero_rates(yield_curve: np.ndarray, dates: np.ndarray, day_counter: np.ndarray, compounding: np.ndarray):
        """
            Calculate the zero rates from a given yield curve.
        :param yield_curve: Yield curve object
        :param dates: Dates for which to calculate the zero rates
        :param day_counter: Day counter name
        :param compounding: Compounding frequency
        :return: Zero rates for the given dates
        """
        return qlyield.zero_rates(yield_curve, dates.flatten(), day_counter[0, 0], compounding[0, 0])

    @staticmethod
    def year_fraction(day_counter: np.ndarray, start_date: np.ndarray, end_date: np.ndarray):
        """
            Calculate the year fraction between two dates using a given day counter.
        :param day_counter: Day counter name
        :param start_date: Start date
        :param end_date: End date
        :return: Year fraction between the two dates
        """
        return qlmisc.year_fraction(day_counter[0, 0], start_date[0, 0], end_date[0, 0])

    @staticmethod
    def forward_curve(dates: np.ndarray, rates: np.ndarray, day_counter: np.ndarray, calendar: np.ndarray):
        """
            Create a forward curve from given dates and rates.
        :param dates: Dates for the forward curve
        :param rates: Rates for the forward curve
        :param day_counter: Day counter name
        :param calendar: Calendar name
        :return: Forward curve object
        """
        return qlyield.forward_curve(dates.flatten(), rates.flatten(), day_counter[0, 0], calendar[0, 0])

    @staticmethod
    def schedule(start_date: np.ndarray, end_date: np.ndarray, tenor: np.ndarray, calendar: np.ndarray, bdc: np.ndarray, end_date_bdc: np.ndarray, date_generation_rule: np.ndarray, end_of_month: np.ndarray):
        """
            Create a schedule of dates based on the given parameters.
        :param start_date: Start date of the schedule
        :param end_date: End date of the schedule
        :param tenor: Tenor for the schedule
        :param calendar: Calendar name
        :param bdc: Business day convention
        :param end_date_bdc: End date business day convention
        :param date_generation_rule: Date generation rule
        :param end_of_month: End of month flag
        :return: Schedule object
        """
        ql_schedule = qlmisc.schedule(start_date[0, 0], end_date[0, 0], tenor[0, 0], calendar[0, 0], bdc[0, 0], end_date_bdc[0, 0], date_generation_rule[0, 0], end_of_month[0, 0])
        return ql_schedule
