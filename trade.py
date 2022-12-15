import requests, json
from time import sleep
from indicators import ema, sma
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import signal
import sys

base_url = "https://api.gemini.com/v1"
has_bought = False
amount_bought = 0
last_update = 0
last_price = 0
profit = 0;
history = []
buy_history = []
sell_history = []
ema_len1_history = []
ema_len2_history = []
ema_len3_history = []

ema_len1 = 9
ema_len2 = 20
ema_len3 = 50

def get_price(coin):
    response = requests.get(base_url + "/pricefeed")
    if response.status_code != 200:
        return None
    prices = response.json()
    for pair in prices:
        if pair['pair'] == coin:
            return float(pair['price'])

def average():
    global history
    if (len(history) < 3):
        return 0
    count = 0
    for i in range(1, 4):
        count += history[len(history) - i]
    return count/3

def buy_conditions(price, ema1, ema2, ema3):
    return ema3 < ema2 and ema2 < ema1 and price > ema3

def buy(price):
    global amount_bought, has_bought
    amount_bought = price;
    has_bought = True
    print("Buying " + str(amount_bought))

def sell(price):
    global amount_bought, has_bought, profit
    has_bought = False
    profit += (price - amount_bought)
    print("Selling @ " + str(price) + " Net: " + str(price - amount_bought) + " Total: " + str(profit))

def signal_handler(sig, frame):
    print("History: " + str(history))
    print("Buy points: " + str(buy_history))
    print("Sell points: " + str(sell_history))
    print("Ema " + str(ema_len1) + ": " + str(ema_len1_history))
    print("Ema " + str(ema_len2) + ": " + str(ema_len2_history))
    print("Ema " + str(ema_len3) + ": " + str(ema_len3_history))

    x = np.linspace(0, len(history))
    plt.plot(range(0, len(history)), history)
    plt.plot(range(0, len(history)), ema_len1_history)
    plt.plot(range(0, len(history)), ema_len2_history)
    plt.plot(range(0, len(history)), ema_len3_history)
    for i in buy_history:
        plt.text(i, history[i], "buy")
    for i in sell_history:
        plt.text(i, history[i], "sell")
    plt.show()

signal.signal(signal.SIGINT, signal_handler)

index = 0;
while True:
    sleep(2)
    price = get_price("ETHUSD")


    if price == None:
        print("Request failed! Probably a good time to panic!")
        # TODO: Panic!
        continue;

    # wait for enough data
    
    if len(history) < ema_len3*2 and last_price != price:
        # not enough data
        print("Gathering Data [" + str(len(history)) + "/" + str(ema_len3 * 2) + "]")
        last_price = price;
        history.append(price)
        ema_len1_history.append(0)
        ema_len2_history.append(0)
        ema_len3_history.append(0)
        index = index + 1
        continue;
    elif len(history) < ema_len3*2:
        continue;

    ema_calc_1 = ema(history, ema_len1)
    ema_calc_2 = ema(history, ema_len2)
    ema_calc_3 = ema(history, ema_len3)
    
    
    if price != last_price:
        ema_len1_history.append(ema_calc_1)
        ema_len2_history.append(ema_calc_2)
        ema_len3_history.append(ema_calc_3)
        if has_bought == False:
            if buy_conditions(price, ema_calc_1, ema_calc_2, ema_calc_3):
                buy(price)
                buy_history.append(index)
        else:
            if not buy_conditions(price, ema_calc_1, ema_calc_2, ema_calc_3):
                sell(price)
                sell_history.append(index)
    
        print(str(price));
        last_price = price;
        history.append(price)
        index = index + 1
        #print("EMA len1: " + str(ema_calc_1) + "EMA len2: " + str(ema_calc_2))
