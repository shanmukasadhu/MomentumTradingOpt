#Load and import yahoo finance api and gold info
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
symbol = "APX"
data = data = pd.DataFrame(yf.download(symbol)).iloc[-1000:][['Close']]


# Returns from prior day to current day
data['returns'] = np.log(data['Close'] / data['Close'].shift(1))

max_z = -1000
max_m = 0
for m in range(1,30,2):
    print(m)
    # Find sign based on the mean of the last 3 days
    data['%d_day_position'% m] = np.sign(data['returns'].rolling(m).mean())
    # Finds strategy returns
    data['%d_day_strategy'% m] = data['%d_day_position'% m].shift(1) * data['returns']
    
    data["final_strategy_%d"%m] = data[['%d_day_strategy'% m]].dropna().cumsum().apply(np.exp)
    data['buy_and_hold'] = data['returns'].cumsum().apply(np.exp)
    
    z = data["final_strategy_%d"%m].iloc[-1]
    if(z > max_z):
        max_z = z
        max_m = m        
    print(z)
print("Max at "+str(max_m)+" rolling day(s): "+str(max_z))
data[['returns', '%d_day_strategy'%max_m]].dropna().cumsum().apply(np.exp).plot(figsize=(10, 6));
if(data['buy_and_hold'].iloc[-1] > max_z):
    print("Buy-and-hold is the best option")
    