import numpy as np
import pandas as pd

def ema(data, samples):
    if len(data) < 2*samples:
        raise ValueError("not enough data")
    c = 2.0 / (samples + 1)
    current_ema = sma(data[-samples*2:-samples], samples)
    for value in data[-samples:]:
        current_ema = (c * value) + ((1-c) * current_ema)
    return current_ema

def sma(data, samples):
    if len(data) < samples:
        raise ValueError("not enough data")
    return sum(data[-samples:]) / float(samples)

# values = [52, 32, 10, 2]
# print(ema(values, 2))
