def BTU_valuation(coal_price, EBITDA_multiple=3):
    #coal price is newcastle thermal
    #will apply EV/EBITDA valuation for 1 yr time horizon
    #reasonable EBITDA_multiple of 3 
    #EV = mcap + debt - cash
    #mcap = EV - debt + cash
    CASH = 548
    DEBT = 1350
    #calculate EBITDA
    #2021 Q2 production numbers
    SEABORNE_MET_EBITDA = 1.4 * -19
    PRB_EBITDA = 22.5 * 2
    SEABORNE_THERMAL = 4.1
    OTHER_US_THERMAL = 3.9
    THERMAL_EBITDA = (SEABORNE_THERMAL + OTHER_US_THERMAL) * (coal_price - 30)
    Q_EBITDA = SEABORNE_MET_EBITDA + PRB_EBITDA + THERMAL_EBITDA
    Y_EBITDA = 4 * Q_EBITDA

    EV = (3 * Y_EBITDA)
    mcap = EV - DEBT + CASH
    return mcap