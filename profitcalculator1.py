import pandas as pd

price_path = 'ER_Outrights_daily.csv'
allocation_path = 'AllocationData.csv'

price__df = pd.read_csv(price_path)
allocation_df = pd.read_csv(allocation_path)
qty = 100
profit = 0
allocation = allocation_df.values
prices = price__df.values
from_date = allocation[0][0]
to_date = allocation[len(allocation)-1][0]
row_number_from_date = price__df.loc[price__df['Date'] == from_date].index[0]
row_number_to_date = price__df.loc[price__df['Date'] == to_date].index[0]
total_qty = []
profits = []
for i in range(1,len(allocation[0])):
    total_qty.append(allocation[0][i]*qty)
for i in range(row_number_from_date+1,row_number_to_date+1):
    row_profit = []
    row_profit.append(allocation[i-row_number_from_date][0])
    for j in range(1,len(allocation[i-row_number_from_date])):
            row_profit.append(round(total_qty[j-1]*(prices[i][j+1]-prices[i-1][j+1]),2))
            total_qty[j-1] = allocation[i-row_number_from_date][j]*qty
    profits.append(row_profit)
df = pd.DataFrame(profits)
df.to_csv("profits.csv",index=False,header=False)