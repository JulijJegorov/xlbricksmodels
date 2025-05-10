"""
    Author: julij
    Date: 04/05/2025
    Description: Vanilla commodity option pricing using QuantLib
"""

import numpy as np
import pandas as pd
import QuantLib as ql
from typing import Any
from scipy.stats import norm
from datetime import datetime
import QuantSpace.libs.qlutils as qlu


def comdty_vanilla_option(evaluation_date: datetime, expiry_date: datetime, forward_price: float, strike_price: float, option_type: str, exercise_type: str, steps: int, volatility: Any, yield_curve: Any):
    """
         Vanilla commodity option pricing using QuantLib
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
    ql.Settings.instance().evaluationDate = qlu.py_to_ql_date(evaluation_date)
    expiry_date = qlu.py_to_ql_date(expiry_date)
    volatility = ql.BlackVolTermStructureHandle(volatility)
    yield_curve = ql.YieldTermStructureHandle(yield_curve)
    option_type_ql = ql.Option.Call if option_type.upper() == 'CALL' else ql.Option.Put

    process = ql.BlackProcess(ql.QuoteHandle(ql.SimpleQuote(forward_price)), yield_curve, volatility)
    payoff = ql.PlainVanillaPayoff(option_type_ql, strike_price)

    if exercise_type.upper() == 'AMERICAN':
        exercise = ql.AmericanExercise(qlu.py_to_ql_date(evaluation_date), expiry_date)
        engine = ql.BinomialCRRVanillaEngine(process, int(steps))
        option = ql.VanillaOption(payoff, exercise)
        option.setPricingEngine(engine)
        option_vega = estimate_vega(option, process, volatility, strike_price, expiry_date, steps)
        option_rho = estimate_rho(option, process, yield_curve, volatility, expiry_date, steps)
    else:
        engine = ql.AnalyticEuropeanEngine(process)
        option = ql.EuropeanOption(payoff, ql.EuropeanExercise(expiry_date))
        option.setPricingEngine(engine)
        option_vega = option.vega()
        option_rho = option.rho()

    result_frame = pd.DataFrame([option.NPV(), option.delta(), option.gamma(), option.theta(), option_vega, option_rho],
                                columns=[option_type], index=['price', 'delta', 'gamma', 'theta', 'vega', 'rho'])
    return result_frame


def comdty_vanilla_option_delta(evaluation_date: datetime, expiry_date: datetime, forward_price: float, delta: float, option_type: str, volatility: Any, yield_curve: Any):
    """
        Vanilla commodity option pricing using QuantLib given options delta
    :param evaluation_date: Date of evaluation
    :param expiry_date: Date of expiry
    :param forward_price: Forward price of the underlying asset
    :param delta: Delta of the option
    :param option_type: CALL or PUT
    :param volatility: Volatility term structure
    :param yield_curve: Yield term structure
    :return: DataFrame with option price, delta, gamma, theta, vega, rho, derived strike price
            and helper values like d1, risk-free rate, atm volatility, years_to_maturity
    """

    expiry_date_ql = qlu.py_to_ql_date(expiry_date)
    evaluation_date_ql = qlu.py_to_ql_date(evaluation_date)
    day_counter = yield_curve.dayCounter()
    years_to_maturity = day_counter.yearFraction(evaluation_date_ql, expiry_date_ql)

    riskfree_rate = yield_curve.zeroRate(expiry_date_ql, day_counter, ql.Continuous).rate()
    volatility_atm = volatility.blackVol(years_to_maturity, forward_price)

    if option_type.upper() == 'CALL':
        d1 = norm.ppf(delta * np.exp(riskfree_rate * years_to_maturity))
    else:
        d1 = norm.ppf(delta * np.exp(riskfree_rate * years_to_maturity) + 1)

    strike_price = forward_price / np.exp(volatility_atm * np.sqrt(years_to_maturity) * d1 - (0.5 * (volatility_atm ** 2)) * years_to_maturity)

    option_frame = comdty_vanilla_option(evaluation_date, expiry_date, forward_price, strike_price, option_type, 'EUROPEAN', None, volatility, yield_curve)

    strike_frame = pd.DataFrame([d1, riskfree_rate, volatility_atm, years_to_maturity, strike_price],
                                columns=[option_type], index=['d1', 'riskfree_rate', 'volatility_atm', 'years_to_maturity', 'strike_price'])

    result_frame = pd.concat([option_frame, strike_frame], axis=0)
    return result_frame


def comdty_vanilla_option_spread(evaluation_date: datetime, expiry_date: datetime, forward_price: float, strike_price_long: float, strike_price_short: float, option_type: str, exercise_type: str, steps: int,
                                 volatility: Any, yield_curve: Any):
    """
        Vanilla commodity option pricing using QuantLib for a spread of two options
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
    option_price_long = comdty_vanilla_option(evaluation_date, expiry_date, forward_price, strike_price_long, option_type, exercise_type, steps, volatility, yield_curve)
    option_price_short = comdty_vanilla_option(evaluation_date, expiry_date, forward_price, strike_price_short, option_type, exercise_type, steps, volatility, yield_curve)
    option_price_long.columns = [f'{option_price_long.columns[0]}_LONG']
    option_price_short.columns = [f'{option_price_short.columns[0]}_SHORT']
    structure = pd.DataFrame(option_price_long.values - option_price_short.values, columns=[f'{option_type}_SPREAD'], index=['price', 'delta', 'gamma', 'theta', 'vega', 'rho'])
    result_frame = pd.concat([option_price_long, option_price_short, structure], axis=1)
    return result_frame


def comdty_vanilla_option_collar(evaluation_date: datetime, expiry_date: datetime, forward_price: float, strike_price_call_short: float, strike_price_put_long: float, exercise_type: str, steps: int, volatility: Any,
                                 yield_curve: Any):
    """
        Vanilla commodity option pricing using QuantLib for a collar strategy
    :param evaluation_date: Date of evaluation
    :param expiry_date: Expiry date
    :param forward_price: Forward price of the underlying asset
    :param strike_price_call_short: Strike price of a long call option
    :param strike_price_put_long: Strike price of a short put option
    :param exercise_type: EUROPEAN or AMERICAN
    :param steps: Number of steps for the binomial tree (only for American options)
    :param volatility: Volatility term structure
    :param yield_curve: Yield term structure
    :return: DataFrame with option price, delta, gamma, theta, vega, rho for both options and the collar
    """
    call_price = comdty_vanilla_option(evaluation_date, expiry_date, forward_price, strike_price_call_short, 'CALL', exercise_type, steps, volatility, yield_curve)
    put_price = comdty_vanilla_option(evaluation_date, expiry_date, forward_price, strike_price_put_long, 'PUT', exercise_type, steps, volatility, yield_curve)
    structure = pd.DataFrame(put_price.values - call_price.values, columns=['COLLAR'], index=['price', 'delta', 'gamma', 'theta', 'vega', 'rho'])
    result_frame = pd.concat([call_price, put_price, structure], axis=1)
    return result_frame


def comdty_vanilla_option_butterfly(evaluation_date: datetime, expiry_date: datetime, forward_price: float, strike_price_low_long: float, strike_price_middle_short: float, strike_price_high_long: float, option_type: str,
                                    exercise_type: str, steps: int, volatility: Any, yield_curve: Any):
    """
        Vanilla commodity option pricing using QuantLib for a butterfly spread strategy
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
    option_price_low = comdty_vanilla_option(evaluation_date, expiry_date, forward_price, strike_price_low_long, option_type, exercise_type, steps, volatility, yield_curve)
    option_price_middle = comdty_vanilla_option(evaluation_date, expiry_date, forward_price, strike_price_middle_short, option_type, exercise_type, steps, volatility, yield_curve)
    option_price_high = comdty_vanilla_option(evaluation_date, expiry_date, forward_price, strike_price_high_long, option_type, exercise_type, steps, volatility, yield_curve)
    option_price_low.columns = [f'{option_price_low.columns[0]}_LOW']
    option_price_middle.columns = [f'{option_price_middle.columns[0]}_MIDDLE']
    option_price_high.columns = [f'{option_price_high.columns[0]}_HIGH']
    structure = pd.DataFrame(option_price_low.values - 2 * option_price_middle.values + option_price_high.values, columns=[f'{option_type}_BUTTERFLY'], index=['price', 'delta', 'gamma', 'theta', 'vega', 'rho'])
    result_frame = pd.concat([option_price_low, option_price_middle, option_price_high, structure], axis=1)
    return result_frame


def comdty_vanilla_option_calendar_spread(evaluation_date: datetime, expiry_date_long: datetime, expiry_date_short: datetime, forward_price: float, strike_price: float, option_type: str, correlation: float, volatility: Any, yield_curve: Any, paths: int):
    """
        Vanilla commodity option pricing using QuantLib for calendar spread options
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

    evaluation_date = qlu.py_to_ql_date(evaluation_date)
    ql.Settings.instance().evaluationDate = evaluation_date

    expiry_date_long = qlu.py_to_ql_date(expiry_date_long)
    expiry_date_short = qlu.py_to_ql_date(expiry_date_short)
    volatility = ql.BlackVolTermStructureHandle(volatility)
    yield_curve = ql.YieldTermStructureHandle(yield_curve)

    correlation_matrix = ql.Matrix(2, 2)
    correlation_matrix[0][0] = 1.0
    correlation_matrix[1][1] = 1.0
    correlation_matrix[0][1] = correlation_matrix[1][0] = correlation

    volatility_long = volatility.blackVol(expiry_date_long, forward_price)
    volatility_short = volatility.blackVol(expiry_date_short, forward_price)

    volatility_term_structure_long = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(evaluation_date, volatility.calendar(), volatility_long, volatility.dayCounter()))
    volatility_term_structure_short = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(evaluation_date, volatility.calendar(), volatility_short, volatility.dayCounter()))

    riskfree_rate_long = yield_curve.zeroRate(expiry_date_long, yield_curve.dayCounter(),  ql.Continuous, ql.NoFrequency).rate()
    riskfree_rate_short = yield_curve.zeroRate(expiry_date_short, yield_curve.dayCounter(),  ql.Continuous, ql.NoFrequency).rate()

    riskfree_rate_term_structure_long = ql.YieldTermStructureHandle(ql.FlatForward(evaluation_date, riskfree_rate_long, yield_curve.dayCounter()))
    riskfree_rate_term_structure_short = ql.YieldTermStructureHandle(ql.FlatForward(evaluation_date, riskfree_rate_short, yield_curve.dayCounter()))

    process_long = ql.BlackProcess(ql.QuoteHandle(ql.SimpleQuote(forward_price)), riskfree_rate_term_structure_long, volatility_term_structure_long)
    process_short = ql.BlackProcess(ql.QuoteHandle(ql.SimpleQuote(forward_price)), riskfree_rate_term_structure_short, volatility_term_structure_short)

    process_array = ql.StochasticProcessArray([process_long, process_short], correlation_matrix)

    num_steps = 365
    day_counter = yield_curve.dayCounter()
    expiry_date_min = np.min([expiry_date_long, expiry_date_short])
    risk_free_rate = riskfree_rate_long if expiry_date_min == expiry_date_long else riskfree_rate_short
    years_to_maturity = day_counter.yearFraction(evaluation_date, expiry_date_min)
    time_grid = ql.TimeGrid(years_to_maturity, num_steps)
    random_sequence_generator = ql.GaussianRandomSequenceGenerator(ql.UniformRandomSequenceGenerator(2 * num_steps, ql.UniformRandomGenerator()))
    gaussian_path_generator = ql.GaussianMultiPathGenerator(process_array, list(time_grid), random_sequence_generator, False)

    contract_long = list()
    contract_short = list()
    for _ in range(int(paths)):
        generated_path = gaussian_path_generator.next().value()
        contract_long.append(generated_path[0][-1])
        contract_short.append(generated_path[1][-1])

    contract_long = np.array(contract_long)
    contract_short = np.array(contract_short)
    spread = contract_long - contract_short

    if option_type.upper() == 'CALL':
        payoff = np.mean(np.clip(spread - strike_price, a_min=0, a_max=None))
    else:
        payoff = np.mean(np.clip(strike_price - spread, a_min=0, a_max=None))

    discount_factor = np.exp(-risk_free_rate * years_to_maturity)
    price = payoff * discount_factor

    result_frame = pd.DataFrame([price, payoff, riskfree_rate_long, riskfree_rate_short, volatility_long, volatility_short],
                                columns=[option_type], index=['price', 'payoff', 'risk_free_rate_long', 'risk_free_rate_short', 'volatility_long', 'volatility_short'])

    return result_frame


def estimate_vega(option: ql.Option, process: ql.BlackProcess, volatility: ql.BlackVolTermStructureHandle, strike_price: float, expiry_date: ql.Date, steps: int, bump: float = 0.01):
    """
        Estimates Vega using finite difference method
    :param option: Option object
    :param process: Black process object
    :param volatility: Volatility term structure
    :param strike_price: Strike price of the option
    :param expiry_date: Expiry date of the option
    :param steps: Number of steps for the binomial tree
    :param bump: Amount to bump the volatility for finite difference
    :return: Vega of the option"""

    evaluation_date = ql.Settings.instance().evaluationDate

    bumped_vol_up = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(
         evaluation_date, volatility.calendar(), volatility.blackVol(expiry_date, strike_price) + bump, volatility.dayCounter()))
    process_up = ql.BlackProcess(ql.QuoteHandle(ql.SimpleQuote(process.x0())), process.riskFreeRate(), bumped_vol_up)
    engine_up = ql.BinomialCRRVanillaEngine(process_up, int(steps))
    option.setPricingEngine(engine_up)
    price_up = option.NPV()

    bumped_vol_down = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(
        evaluation_date, volatility.calendar(), volatility.blackVol(expiry_date, strike_price) - bump, volatility.dayCounter()))
    process_down = ql.BlackProcess(ql.QuoteHandle(ql.SimpleQuote(process.x0())), process.riskFreeRate(), bumped_vol_down)
    engine_down = ql.BinomialCRRVanillaEngine(process_down, int(steps))
    option.setPricingEngine(engine_down)
    price_down = option.NPV()

    vega = (price_up - price_down) / (2 * bump)
    return vega


def estimate_rho(option: ql.Option, process: ql.BlackProcess, yield_curve: ql.YieldTermStructureHandle, volatility: ql.BlackVolTermStructureHandle, expiry_date: ql.Date, steps: int, bump: float = 0.001):
    """ Estimates Rho using finite difference method
    :param option: Option object
    :param process: Black process object
    :param yield_curve: Yield term structure
    :param volatility: Volatility term structure
    :param expiry_date: Expiry date of the option
    :param steps: Number of steps for the binomial tree
    :param bump: Amount to bump the yield for finite difference
    :return: Rho of the option"""

    evaluation_date = ql.Settings.instance().evaluationDate
    base_rate = yield_curve.zeroRate(expiry_date, yield_curve.dayCounter(), ql.Continuous).rate()

    bumped_yield_up = ql.FlatForward(evaluation_date, base_rate + bump, yield_curve.dayCounter())
    process_up = ql.BlackProcess(ql.QuoteHandle(ql.SimpleQuote(process.x0())), ql.YieldTermStructureHandle(bumped_yield_up), volatility)
    engine_up = ql.BinomialCRRVanillaEngine(process_up, int(steps))
    option.setPricingEngine(engine_up)
    price_up = option.NPV()

    bumped_yield_down = ql.FlatForward(evaluation_date, base_rate - bump, yield_curve.dayCounter())
    process_down = ql.BlackProcess(ql.QuoteHandle(ql.SimpleQuote(process.x0())), ql.YieldTermStructureHandle(bumped_yield_down), volatility)
    engine_down = ql.BinomialCRRVanillaEngine(process_down, int(steps))
    option.setPricingEngine(engine_down)
    price_down = option.NPV()

    rho = (price_up - price_down)/(2 * bump)
    return rho
