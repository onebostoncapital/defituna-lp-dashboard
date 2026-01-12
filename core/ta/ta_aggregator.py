def aggregate_ta_signals(price_series):
    ma20 = calculate_ma20(price_series)
    ma200 = calculate_ma200(price_series)
    crossover = calculate_ma_crossover(price_series)
    ...
