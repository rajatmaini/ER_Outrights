import pandas as pd

price_path = 'ER_Outrights_daily.csv'
allocation_path = 'AllocationData.csv'

price__df = pd.read_csv(price_path)
allocation_df = pd.read_csv(allocation_path)
qty = 0
profit = 0
allocation = allocation_df.values
prices = price__df.values
from_date = allocation[0][0]
to_date = allocation[len(allocation)-1][0]
row_number_from_date = price__df.loc[price__df['Date'] == from_date].index[0]
row_number_to_date = price__df.loc[price__df['Date'] == to_date].index[0]
curr_avg_price = prices[row_number_from_date][2]
print(curr_avg_price)
for i in range(row_number_from_date,row_number_to_date+1):
    if(qty==0):
        qty = allocation[i-row_number_from_date][1]
        curr_avg_price = prices[row_number_from_date][2]
    elif(qty!=allocation[i-row_number_from_date][1]):
        if(qty<0 and allocation[i-row_number_from_date][1]<0):
            qty = qty*-1
            allocation_value = allocation[i-row_number_from_date][1]*-1
            if(qty>allocation_value):
                profit += (curr_avg_price-prices[i][2])*(qty-allocation_value)
                qty = allocation_value*-1
            elif(qty<allocation_value):
                curr_avg_price = round(((curr_avg_price*qty)+(prices[i][2]*(allocation_value-qty)))/allocation_value,3)
                qty = allocation_value*-1
        elif(qty<0 and allocation[i-row_number_from_date][1]>0):
            profit+= (curr_avg_price-prices[i][2])*(qty*-1)
            curr_avg_price = prices[i][2]
            qty = allocation[i-row_number_from_date][1]
        elif(qty>0 and allocation[i-row_number_from_date][1]>0):
            allocation_value = allocation[i-row_number_from_date][1]
            if(qty>allocation_value):
                profit+= (prices[i][2]-curr_avg_price)*(qty-allocation_value)
                qty = qty-allocation_value
            elif(qty<allocation_value):
                curr_avg_price = round(((curr_avg_price*qty)+prices[i][2]*(allocation_value-qty))/allocation_value,3)
                qty = allocation_value
        elif(qty>0 and allocation[i-row_number_from_date][1]<0):
            profit+= (prices[i][2]-curr_avg_price)*qty
            qty = allocation[i-row_number_from_date][1]
            curr_avg_price = prices[i][2]
    elif(allocation[i-row_number_from_date][1]==0):
        if(qty<0):
            profit += (curr_avg_price-prices[i][2])*(qty*-1)
        elif(qty>0):
            profit += (prices[i][2]-curr_avg_price)*(qty)
        qty = 0
print(profit)