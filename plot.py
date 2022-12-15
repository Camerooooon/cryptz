import numpy as np
import matplotlib.pyplot as plt
import subprocess

subprocess.check_call(["stty","-icanon"])
history = [float(i) for i in input("History: ").strip('][').split(', ')]
buy_history = [int(i) for i in input("Buy History: ").strip('][').split(', ')]
sell_history = [int(i) for i in input("Sell History: ").strip('][').split(', ')]
ema_len1_history = [float(i) for i in input("Ema Small History: ").strip('][').split(', ')]
ema_len2_history = [float(i) for i in input("Ema Large History: ").strip('][').split(', ')]
ema_len3_history = [float(i) for i in input("Ema Largest History: ").strip('][').split(', ')]
subprocess.check_call(["stty","icanon"])

print(history)

plt.plot(range(0, len(history)), history)
plt.plot(range(0, len(history)), ema_len1_history)
plt.plot(range(0, len(history)), ema_len2_history)
plt.plot(range(0, len(history)), ema_len3_history)
for i in buy_history:
    plt.text(i, history[i], "buy")
for i in sell_history:
    plt.text(i, history[i], "sell")
plt.show()
