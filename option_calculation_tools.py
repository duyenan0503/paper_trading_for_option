import math
import numpy as np

def norm_cdf(x, loc=0.0, scale=1.0):
    if scale <= 0:
        raise ValueError("scale must be positive")
    z = (x - loc) / scale
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


class PVPricing:

    def eq_forward_pricing(
            underlying_spot: float,
            rate: float,
            div_yield: float,
            repo_rate: float,
            tau: float
    ) -> float:
        """
        Calculate the forward price of an equity underlying based on cost of carry replication (exponential rates).
        :param underlying_spot: Underlying spot price
        :param rate: Interest rate
        :param div_yield: Constant dividend yield
        :param repo_rate: Constant repo rate
        :param tau: forward time to expiry year fraction
        """
        if tau <= 0:
            return np.nan
        drift = (rate - div_yield - repo_rate) * tau
        return underlying_spot * math.exp(drift)

    def bs_fut_pricing(s: float, r: float, q: float, tau: float) -> float:
        """Fair forward/futures price using cost-of-carry model."""
        if tau <= 0:
            return np.nan
        return s * math.exp((r - q) * tau)


    def bs_call_pricing(s: float, k: float, r: float, q: float, tau: float, sigma: float) -> float:
        """
        Calculate the price of a European call option using the Black-Scholes formula.
        :param s: Underlying spot price
        :param k: Option strike price
        :param r: Interest rate
        :param q: Constant dividend yield
        :param tau: Time to maturity (in years' fraction)
        :param sigma: Constant volatility
        :return:
        """
        if tau <= 0 or sigma <= 0:
            return np.nan
        d1 = (math.log(s / k) + (r - q + 0.5 * sigma ** 2) * tau) / (sigma * math.sqrt(tau))
        d2 = d1 - sigma * math.sqrt(tau)
        call_price = s * math.exp(-q * tau) * norm_cdf(d1) - k * math.exp(-r * tau) * norm_cdf(d2)
        return call_price

    def bs_put_pricing(s: float, k: float, r: float, q: float, tau: float, sigma: float) -> float:
        """
        Calculate the price of a European put option using the Black-Scholes formula.
        :param s: Underlying spot price
        :param k: Option strike price
        :param r: Interest rate
        :param q: Constant dividend yield
        :param tau: time to maturity (in years' fraction)
        :param sigma: Constant volatility
        """
        if tau <= 0 or sigma <= 0:
            return np.nan

        d1 = (math.log(s / k) + (r - q + 0.5 * sigma ** 2) * tau) / (sigma * math.sqrt(tau))
        d2 = d1 - sigma * math.sqrt(tau)
        put_price = k * math.exp(-r * tau) * norm_cdf(-d2) - s * math.exp(-q * tau) * norm_cdf(-d1)
        return put_price

    def bs_call_pricing_with_fwd(fwd: float, k: float, r: float, tau: float, sigma: float) -> float:
        """
        Calculate the price of a European call option using the Black-Scholes formula.
        :param fwd: Underlying forward price (to match the given tau maturity)
        :param k: Option strike price
        :param r: Interest rate
        :param tau: Time to maturity (in years' fraction)
        :param sigma: Constant volatility
        :return:
        """
        d1 = (math.log(fwd / k) + 0.5 * sigma ** 2 * tau) / (sigma * math.sqrt(tau))
        d2 = d1 - sigma * math.sqrt(tau)
        call_price = (fwd * norm_cdf(d1) - k * norm_cdf(d2)) * math.exp(-r * tau)
        return call_price

    def bs_put_pricing_with_fwd(fwd: float, k: float, r: float, tau: float, sigma: float) -> float:
        """
        Calculate the price of a European put option using the Black-Scholes formula.
        :param fwd: Underlying forward price (to match the given tau maturity)
        :param k: Option strike price
        :param r: Interest rate
        :param tau: time to maturity (in years' fraction)
        :param sigma: Constant volatility
        """
        d1 = (math.log(fwd / k) + 0.5 * sigma ** 2 * tau) / (sigma * math.sqrt(tau))
        d2 = d1 - sigma * math.sqrt(tau)
        put_price = (k * norm_cdf(-d2) - fwd * norm_cdf(-d1)) * math.exp(-r * tau)
        return put_price

    def bs_call_pricing_with_theofwd_pricing(s: float, k: float, r: float, q: float, repo: float, tau: float, sigma: float) -> float:
         """
         Calculate the price of a European call option using the Black-Scholes formula.
         :param s: Underlying spot price
         :param k: Option strike price
         :param r: Interest rate
         :param q: Constant dividend yield
         :param repo: Constant implied repo rate
         :param tau: Time to maturity (in years' fraction)
         :param sigma: Constant volatility
         :return:
         """
         fwd = PVPricing.eq_forward_pricing(s, r, q, repo, tau)
         call_price = PVPricing.bs_call_pricing_with_fwd(fwd, k, r, tau, sigma)
         return call_price


    def bs_put_pricing_with_theofwd_pricing(s: float, k: float, r: float, q: float, repo: float, tau: float, sigma: float) -> float:
          """
          Calculate the price of a European put option using the Black-Scholes formula.
          :param s: Underlying spot price
          :param k: Option strike price
          :param r: Interest rate
          :param q: Constant dividend yield
          :param repo: Constant implied repo rate
          :param tau: time to maturity (in years' fraction)
          :param sigma: Constant volatility
          """
          fwd = PVPricing.eq_forward_pricing(s, r, q, repo, tau)
          put_price = PVPricing.bs_put_pricing_with_fwd(fwd, k, r, tau, sigma)
          return put_price


