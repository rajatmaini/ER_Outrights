import pandas as pd
from datetime import timedelta,datetime

def is_third_monday_in_expiry_month(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    date_obj2 = date_obj+timedelta(days=2)
    if(date_obj.month == 3 or date_obj.month == 6 or date_obj.month == 9 or date_obj.month == 12) :
        if 15 <= date_obj2.day <= 21 and date_obj2.weekday() == 2:
            return True
        else:
            return False
    else:
        False

from_date = "2015-10-28"
to_date = "2015-12-14"
prices_path = "ER_Outrights_daily.csv"
anti_roll_path = f'calculation\AllocationDataAntiRoll_{from_date}_{to_date}.csv'
roll_path = f'calculation\AllocationDataRoll_{from_date}_{to_date}.csv'
 
anti_roll_df=pd.read_csv(anti_roll_path)
roll_df=pd.read_csv(roll_path)
prices_df = pd.read_csv(prices_path)


row_number_from_date = prices_df.loc[prices_df['Date'] == from_date].index[0]
row_number_to_date = prices_df.loc[prices_df['Date'] == to_date].index[0]

total_profits = []
def anti_roll():
    for i in range(row_number_from_date,row_number_to_date):
        profit_perday = []
        prices_1 = prices_df.iloc[i].tolist()
        prices_2 = prices_df.iloc[i+1].tolist()
        profit_perday.append(prices_2[0])
        allocation_list = anti_roll_df.iloc[i-row_number_from_date].tolist()
        for j in range(1,len(allocation_list)):
            if(j<=18):
                profit = (prices_2[j]-prices_1[j])*allocation_list[j]*100
                profit_perday.append(round(profit,3))
            else:
                profit = (prices_1[j-18]-prices_2[j-18])*allocation_list[j]*100
                profit_perday.append(round(profit,3))
        total_profits.append(profit_perday)
    total_profits_df = pd.DataFrame(total_profits,columns=['Date','FEIcm1', 'FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18','Inverse of FEIcm1', 'Inverse of FEIcm2', 'Inverse of FEIcm3', 'Inverse of FEIcm4', 'Inverse of FEIcm5', 'Inverse of FEIcm6', 'Inverse of FEIcm7', 'Inverse of FEIcm8', 'Inverse of FEIcm9', 'Inverse of FEIcm10', 'Inverse of FEIcm11', 'Inverse of FEIcm12', 'Inverse of FEIcm13', 'Inverse of FEIcm14', 'Inverse of FEIcm15', 'Inverse of FEIcm16', 'Inverse of FEIcm17', 'Inverse of FEIcm18'])
    total_profits_df.to_csv(f'profits\AntiRoll_{from_date}_{to_date}.csv')
    total_profits.clear()

def roll():
    for i in range(row_number_from_date,row_number_to_date):
        profit_perday = []
        prices_1 = prices_df.iloc[i].tolist()
        prices_2 = prices_df.iloc[i+1].tolist()
        profit_perday.append(prices_2[0])
        allocation_list = roll_df.iloc[i-row_number_from_date].tolist()
        for j in range(1,len(allocation_list)):
            if(j<=18):
                profit = (prices_2[j+1]-prices_1[j+1])*allocation_list[j]*100
                profit_perday.append(round(profit,3))
            else:
                profit = (prices_1[j-18+1]-prices_2[j-18+1])*allocation_list[j]*100
                profit_perday.append(round(profit,3))
        total_profits.append(profit_perday)
    total_profits_df = pd.DataFrame(total_profits,columns=['Date','FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18','FEIcm19', 'Inverse of FEIcm2', 'Inverse of FEIcm3', 'Inverse of FEIcm4', 'Inverse of FEIcm5', 'Inverse of FEIcm6', 'Inverse of FEIcm7', 'Inverse of FEIcm8', 'Inverse of FEIcm9', 'Inverse of FEIcm10', 'Inverse of FEIcm11', 'Inverse of FEIcm12', 'Inverse of FEIcm13', 'Inverse of FEIcm14', 'Inverse of FEIcm15', 'Inverse of FEIcm16', 'Inverse of FEIcm17', 'Inverse of FEIcm18','Inverse of FEIcm19'])
    total_profits_df.to_csv(f'profits\Roll_{from_date}_{to_date}.csv')
    total_profits.clear()
roll()
anti_roll()
