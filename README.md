**Generate and Monitor simple option portfolio with Excel for Paper Trading**

**Project Purpose**

* Build a portfolio monitoring tool that combines risk sensitivities (Greeks) and scenario-based valuation (PV analysis) to track both current exposure and potential PnL under market changes.
* It helps identify directional risk, volatility exposure, and non-linear effects while also simulating how the portfolio performs under different spot and volatility shocks for better risk management and decision-making.
* Refer to the attached photos and instructions to create the porfolio and generate output reports for the risk and present value impact. 
* Bloomberg access in Excel is required. 


**High-level Description**
Input: paper_simulation.xlsx [sheet: portfolio]
                  |
Processors: 4 python files: greek_calculation.py, greeks_tool.py, pv_calculation.py, pv_calculation_tools.py
                  |
Output: my_risk_report_{date}.xlsx, pv_scenario_{date}.xlsx, sensitivity_tables_{date}.xlsx


**Portfolio sample**
<img width="1570" height="391" alt="image" src="https://github.com/user-attachments/assets/a7e3d194-8cb9-4c86-96b6-d8bbae6ea175" />

<img width="1600" height="410" alt="image" src="https://github.com/user-attachments/assets/a85f1489-31c4-4834-83a9-5ec75f9f1b0d" />

**Output sample**
* Risks sensitiviness (Greeks)
<img width="1834" height="310" alt="image" src="https://github.com/user-attachments/assets/4531f216-c240-408a-9728-e8a71a2088dc" />

* Scenario-based evaluation
<img width="1860" height="370" alt="image" src="https://github.com/user-attachments/assets/f9597a44-f2af-4d74-9c8e-169f4ab2af04" />

<img width="1151" height="673" alt="image" src="https://github.com/user-attachments/assets/4f0b9044-84f8-4fe5-8dd0-06ea61e9ceb4" />

**Instruction**

**Step 1**: Go to build_port_instruction -> Read excel_port_generation_instruction to understand the logic and how to generate the portfolio on Excel + open paper_simulation.xlsx for reference 

**Step 2**: Run 4 python files: greeks_tool.py, greek_calculation.py, pv_calculation_tools.py, pv_calculation.py as the major codes on Python (e.g: PyCharm)

* greek_calculation and greeks_tool are used to calculate key risk sensitivities (Greeks) for each position to monitor how the portfolio reacts to market changes. 
* pv_calculation_tools.py and pv_calculation.py are used to compute current portfolio value and simulate PnL under different market scenarios (spot & volatility shocks).

**Step 3:**  Go to outputs -> my_risk_report_{date}.xlsx from greeks_tool.py and greek_caclulation.py **+** sensitivity_tables_{date}.py and pv_sceraios_{date}.py from  pv_calculation_tools.py and pv_calculation.py

**Disclaimer**: This project is for reference purpose only. It does not constitute investment advice or recommendations.
