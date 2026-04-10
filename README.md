**Generate and Monitor simple option portfolio with Excel for Paper Trading**

<img width="1570" height="391" alt="image" src="https://github.com/user-attachments/assets/a7e3d194-8cb9-4c86-96b6-d8bbae6ea175" />


<img width="1151" height="673" alt="image" src="https://github.com/user-attachments/assets/4f0b9044-84f8-4fe5-8dd0-06ea61e9ceb4" />


**1. Project Purpose**

* Build a portfolio monitoring tool that combines **risk sensitivities (Greeks)** and **scenario-based valuation (PV analysis)** to track both current exposure and potential PnL under market changes.
* It helps better risk management and decision making by:
  - Identifying **directional risk, volatility exposure, and non-linear effects**, which is shown in **my_risk_report_{date}.xlsx**.
  - Simulating how the **portfolio performs** under **different spot and volatility shocks**, which is shown in **pv_scenario_{date}.xlsx, sensitivity_tables_{date}.xlsx**.
* At the same time, the project also provides:
  - The daily snapshot of calculated price options (according to Black Scholes formula) and futures for each date. This is shown in **calculated_price_{date}.xlsx**.
  - The daily snaptshot of options' greeks taken from Bloomberg for reference, which is shown in **BBG_Greeks_ref_{date}.xlsx**. Purpose: Cross check with calculated greeks in my_risk_report_{date}.
  - The daily snapshot of PnL of the portfolio, which is shown in **PnL_Calc_{date}.xlsx**.

**Note:**
* Refer to the attached photos and instructions to create the porfolio and generate output reports for the risk and present value impact. 
* Bloomberg access in Excel is required. 
* The logic behind calculation of options & futures and greeks are explained in separate documents named **option_and_future_calc_explain** and **greeks_calc_explain** in build_port_instruction. 


**2. High-level Description**

          **Input**: paper_simulation.xlsx with 3 main sheets: portfolio, PnL_Calc, BBG_Greeks
                                
                                
                                                  |
                                                  V
                                                  
         **Processors**: 4 python files: greek_calculation.py, greeks_tool.py, pv_calculation.py, pv_calculation_tools.py
                                                  
                                                  |
                                                  V
                                                  
         ** Main Output**: my_risk_report_{date}.xlsx, pv_scenario_{date}.xlsx, sensitivity_tables_{date}.xlsx
         **Side Output**: calculated_price_{date}.xlsx, BBG_Greeks_ref_{date}.xlsx, PnL_Calc_{date}.xlsx



**3. Instruction**

**Step 1**: Go to build_port_instruction -> Read excel_port_generation_instruction, option_and_future_calc_explain, greeks_calc_explain to understand the logic and how to generate the portfolio on Excel **+** open paper_simulation.xlsx for reference 

**Step 2**: Run 4 python files: greeks_tool.py, greek_calculation.py, pv_calculation_tools.py, pv_calculation.py as the major codes on Python (e.g: PyCharm)

* greek_calculation and greeks_tool are used to calculate key risk sensitivities (Greeks) for each position to monitor how the portfolio reacts to market changes. 
* pv_calculation_tools.py and pv_calculation.py are used to compute current portfolio value and simulate PnL under different market scenarios (spot & volatility shocks). It also provides the snapshot for 

**Step 3:**  Go to **outputs** -> my_risk_report_{date}.xlsx from greeks_tool.py and greek_caclulation.py **+** sensitivity_tables_{date}.py and pv_sceraios_{date}.py from  pv_calculation_tools.py and pv_calculation.py **+** calculated_price_{date}.xlsx, BBG_Greeks_ref_{date}.xlsx, PnL_Calc_{date}.xlsx

**Disclaimer**: This project is for reference purpose only. It does not constitute investment advice or recommendations.



**4.1. Portfolio sample**
<img width="1570" height="391" alt="image" src="https://github.com/user-attachments/assets/a7e3d194-8cb9-4c86-96b6-d8bbae6ea175" />

<img width="1600" height="410" alt="image" src="https://github.com/user-attachments/assets/a85f1489-31c4-4834-83a9-5ec75f9f1b0d" />

Excel commands are also provided in build_port_instruction/paper_simulation.xlsx

<img width="1891" height="670" alt="image" src="https://github.com/user-attachments/assets/443b6d6d-4d16-43bb-b4b5-56f93afc00b3" />


**4.2. Main Output sample**

* Risks sensitiviness (Greeks)

my_risk_report_{date}.xlsx
<img width="1834" height="310" alt="image" src="https://github.com/user-attachments/assets/4531f216-c240-408a-9728-e8a71a2088dc" />

* Scenario-based evaluation

pv_scenario_{date}.xlsx
<img width="1860" height="370" alt="image" src="https://github.com/user-attachments/assets/f9597a44-f2af-4d74-9c8e-169f4ab2af04" />

sensitivity_tables_{date}.xlsx
<img width="1151" height="673" alt="image" src="https://github.com/user-attachments/assets/4f0b9044-84f8-4fe5-8dd0-06ea61e9ceb4" />


**4.3. Side Output sample**

* calculated_price_{date}.xlsx
  
<img width="1890" height="372" alt="image" src="https://github.com/user-attachments/assets/da41ed27-3cbd-4176-90cb-1ff1807d653b" />

* BBG_Greeks_ref_{date}.xksx

<img width="791" height="390" alt="image" src="https://github.com/user-attachments/assets/e0ddd02e-40b2-4aa5-818b-79e7416e7864" />


* PnL_Calc_{date}.xlsx

<img width="1662" height="412" alt="image" src="https://github.com/user-attachments/assets/6ae6ff39-1ebd-4ff6-bdbe-c182c1294a9f" />

