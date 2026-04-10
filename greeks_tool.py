import numpy as np
from product_and_pricing_tool import PVPricing

class GrePricing:

    @staticmethod
    def bs_delta(sec_type: str, opt_type: str, mifid: str, s: float, spot_fut: float, k: float, r: float, q: float,
                      tau: float, sigma: float, spot_shift = 0.01) -> float:
        """
        Compute cash delta using central finite difference under Black-Scholes.

        :param opt_type: "C" for call, "P" for put
        :param s:        spot
        :param k:        strike
        :param r:        interest rate
        :param q:        dividend yield
        :param tau:      time to maturity
        :param sigma:    volatility
        :param bump:     proportional bump size for spot (default = ±0.25%)
        :return:         cash delta
        """
        if tau <= 0 or mifid == "VOLI":
            return np.nan
        # Spot bumps
        # Price using your existing pricing tools
        if sec_type == "Future":
            spot_fut_up = spot_fut*(1+spot_shift)
            spot_fut_down = spot_fut*(1 - spot_shift)
            pv_up = PVPricing.bs_fut_pricing(spot_fut_up, r, q, tau)
            pv_down = PVPricing.bs_fut_pricing(spot_fut_down, r, q, tau)

            delta = (pv_up - pv_down) / (2*spot_shift*spot_fut)
            return delta

        elif sec_type == "Option" and mifid != "VOLI":
            if sigma <= 0:
                return np.nan

            s_up = s * (1 + spot_shift)
            s_down = s * (1 - spot_shift)
            if opt_type.upper().startswith("C"):
                pv_up = PVPricing.bs_call_pricing(s_up, k, r, q, tau, sigma)
                pv_down = PVPricing.bs_call_pricing(s_down, k, r, q, tau, sigma)
            else:
                pv_up = PVPricing.bs_put_pricing(s_up, k, r, q, tau, sigma)
                pv_down = PVPricing.bs_put_pricing(s_down, k, r, q, tau, sigma)

            delta = (pv_up - pv_down) / (2*spot_shift*s)
            return delta

        else:
            return np.nan



    @staticmethod
    def bs_delta_cash(sec_type: str, opt_type: str, mifid: str, s: float, spot_fut: float, k: float, r: float, q: float,
                 tau: float, sigma: float, spot_shift=0.01) -> float:
        """
        Compute cash delta using central finite difference under Black-Scholes.

        :param opt_type: "C" for call, "P" for put
        :param s:        spot
        :param k:        strike
        :param r:        interest rate
        :param q:        dividend yield
        :param tau:      time to maturity
        :param sigma:    volatility
        :param bump:     proportional bump size for spot (default = ±0.25%)
        :return:         cash delta
        """

        if tau <= 0 or mifid == "VOLI":
            return np.nan
        # Spot bumps

        # Price using your existing pricing tools
        if sec_type == "Option" and mifid != "VOLI":
            s_up = s * (1 + spot_shift)
            s_down = s * (1 - spot_shift)
            if opt_type.upper().startswith("C"):
                pv_up = PVPricing.bs_call_pricing(s_up, k, r, q, tau, sigma)
                pv_down = PVPricing.bs_call_pricing(s_down, k, r, q, tau, sigma)
            else:
                pv_up = PVPricing.bs_put_pricing(s_up, k, r, q, tau, sigma)
                pv_down = PVPricing.bs_put_pricing(s_down, k, r, q, tau, sigma)

        elif sec_type == "Future":
            spot_fut_up = spot_fut * (1 + spot_shift)
            spot_fut_down = spot_fut * (1 - spot_shift)
            pv_up = PVPricing.bs_fut_pricing(spot_fut_up, r, q, tau)
            pv_down = PVPricing.bs_fut_pricing(spot_fut_down, r, q, tau)

        else:
            return np.nan

        # Central difference delta (cash delta)
        delta_cash = (pv_up - pv_down) / (2 * spot_shift) #if delta:  (pv_up - pv_down) / (2 * spot_shift * spot)
        return delta_cash

    @staticmethod
    def bs_vega(sec_type: str, opt_type: str, mifid: str, s: float, k: float, r: float, q: float,
                      tau: float, sigma: float, spot_shift = 0.0025) -> float:

        if tau <= 0:
            return np.nan

        if sec_type == "Option" and mifid == "VOLI":
            spot_weight = 0.5 / (np.sqrt(tau) + np.sqrt(((tau * 360) + 30) / 360))
            s_voli_up = s + spot_shift * 100 * spot_weight
            s_voli_down = s - spot_shift *100 * spot_weight

            if opt_type.upper().startswith("C"):
                pv_up = PVPricing.bs_call_pricing(s_voli_up, k, r, q, tau, sigma)
                pv_down = PVPricing.bs_call_pricing(s_voli_down, k, r, q, tau, sigma)
            else:
                pv_up = PVPricing.bs_put_pricing(s_voli_up, k, r, q, tau, sigma)
                pv_down = PVPricing.bs_put_pricing(s_voli_down, k, r, q, tau, sigma)

            vega = (pv_up - pv_down) / (2 * spot_shift*100)
            return vega

        elif sec_type == "Option" and mifid != "VOLI":
            vol_bump = sigma + 0.005
            vol_down = sigma - 0.005

            if opt_type.upper().startswith("C"):
                pv_up = PVPricing.bs_call_pricing(s, k, r, q, tau, vol_bump)
                pv_down = PVPricing.bs_call_pricing(s, k, r, q, tau, vol_down)
            else:
                pv_up = PVPricing.bs_put_pricing(s, k, r, q, tau, vol_bump)
                pv_down = PVPricing.bs_put_pricing(s, k, r, q, tau, vol_down)
            vega = pv_up - pv_down #for 1% move. If want 100% move in vol, vega = (pv_up = pv_down)/ (0.005*2)
            return vega

        else:
            return np.nan

    @staticmethod
    def bs_theta(sec_type: str, opt_type: str, s: float, spot_fut: float, k: float, r: float, q: float,
                tau: float, sigma: float, theta_shift= 1/360) -> float:

        if tau <= 0:
            return np.nan

        # Price using your existing pricing tools
        tau_td = tau
        tau_tmr = tau - theta_shift

        if sec_type == "Option":
            if opt_type.upper().startswith("C"):
                pv_td = PVPricing.bs_call_pricing(s, k, r, q, tau_td, sigma)
                pv_tmr = PVPricing.bs_call_pricing(s, k, r, q, tau_tmr, sigma)
            else:
                pv_td = PVPricing.bs_put_pricing(s, k, r, q, tau_td, sigma)
                pv_tmr = PVPricing.bs_put_pricing(s, k, r, q, tau_tmr, sigma)

        elif sec_type == "Future":
            pv_td = PVPricing.bs_fut_pricing(spot_fut, r, q, tau_td)
            pv_tmr = PVPricing.bs_fut_pricing(spot_fut, r, q, tau_tmr)

        else:
            return np.nan

        # Central difference delta (cash delta)
        theta = pv_tmr - pv_td
        return theta

    @staticmethod
    def bs_gamma(sec_type: str, opt_type: str, mifid: str, s: float, spot_fut: float, k: float, r: float, q: float,
                 tau: float, sigma: float, spot_shift=0.01) -> float:

            if tau <= 0 or mifid == "VOLI":
                return np.nan

            if sec_type == "Option":
                base = s
            elif sec_type == "Future":
                base = spot_fut
            else:
                return np.nan

            # bumped spots
            u_up = base * (1 + spot_shift)
            u_down = base * (1 - spot_shift)

            # get deltas at bumped levels
            if sec_type == "Option":
                if opt_type.upper().startswith("C"):
                    pv_mid = PVPricing.bs_call_pricing(base, k, r, q, tau, sigma)
                    pv_up = PVPricing.bs_call_pricing(u_up, k, r, q, tau, sigma)
                    pv_down = PVPricing.bs_call_pricing(u_down, k, r, q, tau, sigma)
                else:
                    pv_mid = PVPricing.bs_put_pricing(base, k, r, q, tau, sigma)
                    pv_up = PVPricing.bs_put_pricing(u_up, k, r, q, tau, sigma)
                    pv_down = PVPricing.bs_put_pricing(u_down, k, r, q, tau, sigma)

            elif sec_type == "Future":
                # Standard futures have linear delta (Gamma is theoretically 0)
                pv_mid = PVPricing.bs_fut_pricing(base, r, q, tau)
                pv_up = PVPricing.bs_fut_pricing(u_up, r, q, tau)
                pv_down = PVPricing.bs_fut_pricing(u_down, r, q, tau)

            else:
                return np.nan

                # Standard Finite Difference: (V_up - 2*V_mid + V_down) / h^2
                # Scaled to 1% move: [(V_up - 2*V_mid + V_down) / h^2] * h^2
            return (pv_up - 2 * pv_mid + pv_down)/((base*spot_shift)**2)

    @staticmethod
    def bs_gamma_cash(sec_type: str, opt_type: str, mifid: str, s: float, spot_fut: float, k: float, r: float, q: float,
                 tau: float, sigma: float, spot_shift=0.01) -> float:

        if tau <= 0 or mifid == "VOLI":
            return np.nan

        if sec_type == "Option":
            base = s
        elif sec_type == "Future":
            base = spot_fut
        else:
            return np.nan

        # bumped spots
        u_up = base * (1 + spot_shift)
        u_down = base * (1 - spot_shift)

        # get deltas at bumped levels
        if sec_type == "Option":
            if opt_type.upper().startswith("C"):
                pv_mid = PVPricing.bs_call_pricing(base, k, r, q, tau, sigma)
                pv_up = PVPricing.bs_call_pricing(u_up, k, r, q, tau, sigma)
                pv_down = PVPricing.bs_call_pricing(u_down, k, r, q, tau, sigma)
            else:
                pv_mid = PVPricing.bs_put_pricing(base, k, r, q, tau, sigma)
                pv_up = PVPricing.bs_put_pricing(u_up, k, r, q, tau, sigma)
                pv_down = PVPricing.bs_put_pricing(u_down, k, r, q, tau, sigma)

        elif sec_type == "Future":
            # Standard futures have linear delta (Gamma is theoretically 0)
            pv_mid = PVPricing.bs_fut_pricing(base, r, q, tau)
            pv_up = PVPricing.bs_fut_pricing(u_up, r, q, tau)
            pv_down = PVPricing.bs_fut_pricing(u_down, r, q, tau)
        else:
            return np.nan

            # Standard Finite Difference: (V_up - 2*V_mid + V_down) / h^2
            # Scaled to 1% move: [(V_up - 2*V_mid + V_down) / h^2] * h^2
        return (pv_up - 2 * pv_mid + pv_down)



