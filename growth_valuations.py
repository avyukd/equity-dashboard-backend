import numpy as np

def get_PV_from_income(income, discount_rate):
    CFs = []
    for i in range(len(income)):
        CF = income[i] / ((1 + discount_rate) ** i)
        CFs.append(CF)
    PV = sum(CFs)
    return PV

def get_pltr_valuation(CAGR=0.20, discount_rate=0.08,terminal_growth_rate=0.03, SPEED_OF_CONVERGENCE=2.5):
    REVENUE_2020 = 1071
    OPMARGIN_2020 = -0.80
    TARGET_OP_MARGIN = 0.25
    TAX_RATE = 0.27
    revenues = [REVENUE_2020]
    for i in range(1,11):
        revenues.append(revenues[i-1]*(1+CAGR))
    opmargins = [OPMARGIN_2020]
    for i in range(1,11):
        mult = SPEED_OF_CONVERGENCE/(1+SPEED_OF_CONVERGENCE)
        add = TARGET_OP_MARGIN/(1+SPEED_OF_CONVERGENCE)
        opmargins.append(opmargins[i-1]*mult+add)
    EBIT = np.array(revenues)*np.array(opmargins)
    taxable = []
    carry_losses = 0
    for i in range(0,11):
        if EBIT[i] < 0:
            taxable.append(0)
            carry_losses = carry_losses - EBIT[i]
        else:
            if EBIT[i] > carry_losses:
                taxable.append(EBIT[i]-carry_losses)
            else:
                taxable.append(0)
                carry_losses = carry_losses - EBIT[i]
    taxes_paid = np.array(taxable)*0.27
    income = revenues-taxes_paid
    PV = get_PV_from_income(income, discount_rate)
    return PV

print(get_pltr_valuation(0.3,0.08,0.03,2.5))