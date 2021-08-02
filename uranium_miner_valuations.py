
import numpy as np

def get_PV_from_income(income, discount_rate):
    CFs = []
    for i in range(len(income)):
        CF = income[i] / ((1 + discount_rate) ** i)
        CFs.append(CF)
    PV = sum(CFs)
    return PV

def get_global_atomic_valuation(price, discount_rate=0.08):
    #DASA MINE PHASE 1
    AISC_LB = 18.39
    TAX_LB = 2.09
    CAPEX = 203
    yearly_production = np.array([0, 0, 0, 0.482, 4, 4, 4, 4, 4.4, 4.6, 5.1, 5.1, 4, 2, 1.7, 0.05])
    revenues = yearly_production * price
    total_AISC = yearly_production * AISC_LB
    total_tax = yearly_production * TAX_LB
    total_tax += 1.615
    total_tax[0:6] = 0
    income = revenues - total_AISC - total_tax
    PV = get_PV_from_income(income, discount_rate)
    NPV_DASA_PHASE_1= PV - CAPEX
    #DASA MINE PHASE 2
    NPV_DASA_PHASE_2 = 120
    #ZINC MINE
    #50 million from crux appraisal in 2020
    #150 million from Cormark
    NPV_ZINC_MINE = 100
    #EXPLORATION
    #60 Mlbs, value at 0.5/lb
    NPV_EXPLORATION_MINE = 30
    return NPV_DASA_PHASE_1 + NPV_DASA_PHASE_2 + NPV_ZINC_MINE + NPV_EXPLORATION_MINE

def get_bannerman_energy_valuation(price, discount_rate=0.08):
    AISC_LB = 41
    CAPEX = 254
    yearly_production = np.array([0, 0, 0, 3, 4, 4, 4, 3, 5, 3, 3, 3, 4, 3, 3, 3, 1])
    revenue = yearly_production * price
    total_AISC = yearly_production * AISC_LB
    revenue_minus_total_AISC = revenue - total_AISC
    tax_rate = 0.375
    taxes_paid = revenue_minus_total_AISC * tax_rate
    taxes_paid[0:5] = 0
    income = revenue_minus_total_AISC - taxes_paid
    PV = get_PV_from_income(income, discount_rate)
    NPV_BANNERMAN = PV - CAPEX
    return NPV_BANNERMAN

def get_paladin_energy_valuation(price, discount_rate=0.08):
    RESTART_COST = 81
    yearly_production = np.array([0,3.3,5.5,5.9,5.9,5.9,5.9,5.9,5.9,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,2])
    revenue = yearly_production * price
    production_cash_cost_LB = np.array([0, 23, 27.4, 27.4, 27.4, 27.4, 27.4, 27.4, 27.4, 26.5, 26.5, 26.5, 26.5, 26.5, 26.5, 26.5, 26.5, 26.5])
    freight_logistics_cash_cost_LB = np.array([0, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95])
    sustaining_CAPEX_LB = np.array([0,0.45,2.4,2.4,2.4,2.4,2.4,2.4,2.4,3.7,3.7,3.7,3.7,3.7,3.7,3.7,3.7,3.7])
    OPEX_LB = production_cash_cost_LB + freight_logistics_cash_cost_LB + sustaining_CAPEX_LB
    total_OPEX = yearly_production * OPEX_LB
    op_revenue = revenue - total_OPEX
    royalty_rate = 0.03
    op_revenue_minus_royalty = op_revenue - (op_revenue * royalty_rate)
    tax_rate = 0.375
    taxes_paid = op_revenue_minus_royalty * tax_rate
    income = op_revenue_minus_royalty - taxes_paid
    PV = get_PV_from_income(income, discount_rate)
    NPV_LARGER_HEINRICH = (PV - RESTART_COST)
    NPV_LARGER_HEINRICH_PDN_SHARE = NPV_LARGER_HEINRICH * 0.75
    NPV_EXPLORATION_PROPERTIES = 250 * 0.5
    return NPV_LARGER_HEINRICH_PDN_SHARE + NPV_EXPLORATION_PROPERTIES

def get_denison_mines_valuation(price, discount_rate=0.08):
    #PHOENIX
    OPEX_LB = 3.33
    CAPEX = 322.5
    yearly_production = np.array([0, 0, 0, 0, 2.364, 5.91, 5.91, 5.91, 5.91, 5.91, 5.91, 5.91, 5.91, 5.91, 3.213])
    revenue = yearly_production * price
    total_OPEX = yearly_production * OPEX_LB
    op_revenue = revenue - total_OPEX
    royalty_rate = 0.10
    op_revenue_minus_royalty = op_revenue - (op_revenue * royalty_rate)
    tax_rate = 0.27
    taxes_paid = op_revenue_minus_royalty * tax_rate
    taxes_paid[0:6] = 0
    income = op_revenue_minus_royalty - taxes_paid
    PV = get_PV_from_income(income, discount_rate)
    NPV_PHOENIX = PV - CAPEX
    NPV_PHOENIX_DENISON_SHARE = NPV_PHOENIX * 0.90
    #GRYPHON
    NPV_GRYPHON = 50
    #WATERBURY
    NPV_WATERBURY = 34
    #NET CASH
    NET_CASH = 122
    #PHYSICAL
    NPV_PHYSICAL = 2.5 * price
    #JCU
    NPV_JCU = 25

    return NPV_PHOENIX_DENISON_SHARE + NPV_GRYPHON + NPV_WATERBURY + NPV_PHYSICAL + NPV_JCU + NET_CASH

def get_ur_energy_valuation(price, discount_rate=0.08):
    #NPV Lost Creek
    yearly_production = np.array([0.5,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1])
    revenue = yearly_production * price
    OPEX_LB = 14.58
    CAPEX = 15.4
    total_OPEX = yearly_production * OPEX_LB
    op_revenue = revenue - total_OPEX
    royalty_rate = 0.05
    op_revenue_minus_royalty = op_revenue - (op_revenue * royalty_rate)
    TAX_LB = 7.32
    taxes_paid = yearly_production * TAX_LB
    income = op_revenue_minus_royalty - taxes_paid
    PV = get_PV_from_income(income, discount_rate)
    NPV_LOST_CREEK = PV - CAPEX
    #NPV Shirley Basin
    yearly_production = np.array([0,0.5,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75])
    revenue = yearly_production * price
    OPEX_LB = 14.30
    CAPEX = 26.2
    total_OPEX = yearly_production * OPEX_LB
    op_revenue = revenue - total_OPEX
    royalty_rate = 0.05
    op_revenue_minus_royalty = op_revenue - (op_revenue * royalty_rate)
    taxes_paid = op_revenue_minus_royalty * 0.15
    income = op_revenue_minus_royalty - taxes_paid
    PV = get_PV_from_income(income, discount_rate)
    NPV_SHIRLEY_BASIN = PV - CAPEX
    #NET DEBT
    NET_CASH = 12
    #other projects
    NPV_OTHER = 20
    return NPV_LOST_CREEK + NPV_SHIRLEY_BASIN + NPV_OTHER + NET_CASH

def get_azarga_valuation(price, discount_rate=0.08):
    #NPV Dewey Burdock
    CAPEX = 31.672
    yearly_production = np.array([0,0,0,0.1260,0.5020,1.0090,1.0090,1.0090,1.0090,0.9460,1.0090,1.0090,1.0090,1.0090,1.0090,1.0090,1.0090,1.0090,0.6310])
    revenue = yearly_production * price
    AISC_LB = 28.88
    total_AISC = yearly_production * AISC_LB
    op_revenue = revenue - total_AISC
    tax_rate = 0.15
    taxes_paid = op_revenue * tax_rate
    income = op_revenue - taxes_paid
    PV = get_PV_from_income(income, discount_rate)
    NPV_DEWEY_BURDOCK = PV - CAPEX
    #NPV Gas Hills
    yearly_production = np.array([0,0,0,0,0,0.5,1,1,1,1,1,1,1,1,0.5])
    revenue = yearly_production * price
    AISC_LB = 30
    total_AISC = yearly_production * AISC_LB
    op_revenue = revenue - total_AISC
    tax_rate = 0.15
    taxes_paid = op_revenue * tax_rate
    income = op_revenue - taxes_paid
    PV = get_PV_from_income(income, discount_rate)
    NPV_GAS_HILLS = PV * 0.5
    #NPV Centennial
    CAPEX = 71
    yearly_production = np.array([0.0000,0.0000,0.0000,0.7000,0.7000,0.7000,0.7000,0.7000,0.7000,0.7000,0.7000,0.7000])
    revenue = yearly_production * price
    AISC_LB = 40.24
    total_AISC = yearly_production * AISC_LB
    op_revenue = revenue - total_AISC
    tax_rate = 0.15
    taxes_paid = op_revenue * tax_rate
    income = op_revenue - taxes_paid
    PV = get_PV_from_income(income, discount_rate)
    NPV_CENTENNIAL = PV - CAPEX
    if NPV_CENTENNIAL < 0:
        NPV_CENTENNIAL = 5
    NPV_JUNIPER = 3
    return NPV_DEWEY_BURDOCK + NPV_GAS_HILLS + NPV_CENTENNIAL + NPV_JUNIPER