from openpyxl.formatting.rule import ColorScaleRule
import numpy as np
from openpyxl.reader.excel import load_workbook
from openpyxl.styles import Font
from misc import DBConfig
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, StrMethodFormatter
from product_and_pricing_tool import PVPricing
from openpyxl import load_workbook
import os
from greeks_tool import GrePricing
from openpyxl.styles import Font, Alignment
from datetime import date


curr_path = os.path.abspath(__file__)
curr_dir = os.path.dirname(curr_path)
parent_dir = os.path.join(curr_dir, os.pardir)
today_str = date.today().strftime("%Y%m%d")
today_col = date.today().strftime("%Y/%m/%d")
"""
INPUT PARAMETERS
"""
input_param_path = curr_dir + r'\inputs\paper_simulation.xlsx'
df: pd.Series = pd.read_excel(
    io=input_param_path,
    sheet_name='portfolio',
    header=0,
    index_col=0
).squeeze().reset_index().rename(columns={"index": "BloombergCode"})

"""
FETCH DATA
"""

col_s = "OPT_UNDL_PX"
col_s_fut = "Undl_fut_px_last"
col_k = "OPT_STRIKE_PX"
col_r = "Cash_rate"
col_tau = "TTM"
col_sigma = "IVOL_MID"
col_q = "EQY_DVD_YLD_EST"
col_sec = "SECURITY_TYP2"
col_mifid = "MIFID_UNDERLYING_DERIVATIVE_TYPE"
col_mid = "PX_MID"
col_opt = "OPT_PUT_CALL"
col_position = "Position"

required_cols = [col_s, col_k, col_r, col_tau, col_sigma, col_q]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise KeyError(f"Required columns missing from DataFrame: {missing}\n"
                   f"Existing columns: {list(df.columns)}")



cols_to_fix = [col_sec, col_opt, col_mifid]
for c in cols_to_fix:
    df[c] = df[c].astype(str)

# Central difference with spot_shift = 0.01 for each side
def compute_row_delta(row):

    delta = GrePricing.bs_delta(
        sec_type=row[col_sec],
        opt_type=row[col_opt],
        mifid=row[col_mifid],
        s=row[col_s],
        spot_fut=row[col_s_fut],
        k=row[col_k],
        r=row[col_r],
        q=row[col_q],
        tau=row[col_tau],
        sigma=row[col_sigma]
    ) * row[col_position]

    return delta
df["Delta"] = df.apply(compute_row_delta, axis=1)

# Delta * base
def compute_row_delta_cash(row):
    delta_cash = GrePricing.bs_delta_cash(
        sec_type=row[col_sec],
        opt_type=row[col_opt],
        mifid=row[col_mifid],
        s=row[col_s],
        spot_fut=row[col_s_fut],
        k=row[col_k],
        r=row[col_r],
        q=row[col_q],
        tau=row[col_tau],
        sigma=row[col_sigma]
    ) * row[col_position]

    return delta_cash
df["Delta_Cash"] = df.apply(compute_row_delta_cash, axis=1)

# For normal option: Central difference with spot_shift = 0.005 for each side
# For VIX, s +/- spot_shift * 100 * spot_weight with spot_shift = 0.0025
def compute_row_vega(row):
    vega = GrePricing.bs_vega(
        sec_type=row[col_sec],
        opt_type=row[col_opt],
        mifid=row[col_mifid],
        s=row[col_s],
        k=row[col_k],
        r=row[col_r],
        q=row[col_q],
        tau=row[col_tau],
        sigma=row[col_sigma]
    )* row[col_position]

    return vega
df["Vega"] = df.apply(compute_row_vega, axis=1)

#shift for 1 day
def compute_row_theta(row):
    theta = GrePricing.bs_theta(
        sec_type=row[col_sec],
        opt_type=row[col_opt],
        s=row[col_s],
        spot_fut=row[col_s_fut],
        k=row[col_k],
        r=row[col_r],
        q=row[col_q],
        tau=row[col_tau],
        sigma=row[col_sigma]
    ) * row[col_position]

    return theta
df["Theta"] = df.apply(compute_row_theta, axis=1)

#math gamma
def compute_row_gamma(row):
    gamma = GrePricing.bs_gamma(
        sec_type=row[col_sec],
        opt_type=row[col_opt],
        mifid=row[col_mifid],
        s=row[col_s],
        spot_fut=row[col_s_fut],
        k=row[col_k],
        r=row[col_r],
        q=row[col_q],
        tau=row[col_tau],
        sigma=row[col_sigma]
    ) * row[col_position]

    return gamma
df["Gamma"] = df.apply(compute_row_gamma, axis=1)

#Dollar_curvature
def compute_row_gamma_cash(row):
    gamma = GrePricing.bs_gamma_cash(
        sec_type=row[col_sec],
        opt_type=row[col_opt],
        mifid=row[col_mifid],
        s=row[col_s],
        spot_fut=row[col_s_fut],
        k=row[col_k],
        r=row[col_r],
        q=row[col_q],
        tau=row[col_tau],
        sigma=row[col_sigma]
    ) * row[col_position]

    return gamma
df["Gamma_Cash"] = df.apply(compute_row_gamma_cash, axis=1)
df.insert(0, "AsOfDate", today_col)

cols_to_show = [
    "AsOfDate",
    "BloombergCode",
    col_sec,
    col_position,
    "OPT_UNDL_TICKER/UNDL_SPOT_TICKER",
    "MIFID_UNDERLYING_ASSET_CLASS",
    col_mifid,
    col_tau,
    "Delta",
    "Delta_Cash",
    "Vega",
    "Theta",
    "Gamma",
    "Gamma_Cash"
]


df[cols_to_show].to_excel(curr_dir + fr'\outputs\\{today_str}\\my_risk_report_{today_str}.xlsx', index=False)
