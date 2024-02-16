import pandas as pd
from datetime import timedelta,datetime
import matplotlib.pyplot as plt

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

figure = plt.figure()
ax1 = figure.add_subplot(2, 2, 1)
ax2 = figure.add_subplot(2, 2, 2)


from_date = "2023-01-02"
to_date = "2023-11-30"
prices_path = "ER_Outrights_daily.csv"
anti_roll_path = f'calculation\AllocationDataAntiRoll_{from_date}_{to_date}.csv'
roll_path = f'calculation\AllocationDataRoll_{from_date}_{to_date}.csv'
 
anti_roll_df=pd.read_csv(anti_roll_path)
roll_df=pd.read_csv(roll_path)
prices_df = pd.read_csv(prices_path)

period = 20
row_number_from_date = prices_df.loc[prices_df['Date'] == from_date].index[0]
row_number_to_date = prices_df.loc[prices_df['Date'] == to_date].index[0]

total_profits = []
figure.suptitle(f'{from_date}_{to_date}_Period {period}', fontsize=16)

def anti_roll():
    change_expiry = False
    expiry_price_1 = 0
    for i in range(row_number_from_date,row_number_to_date+1):
        profit_perday = []
        prices_1 = prices_df.iloc[i].tolist()
        if((i+period)>=len(prices_df)):
            break
        prices_2 = prices_df.iloc[i+period].tolist()
        profit_perday.append(prices_2[0])
        
        if(is_third_monday_in_expiry_month(prices_2[0])):
            change_expiry =True
            expiry_price_1 = prices_2[1]
        if(is_third_monday_in_expiry_month(prices_df.iloc[i-1].tolist()[0])):
            change_expiry = False
            expiry_price_1 = 0
        allocation_list = anti_roll_df.iloc[i-row_number_from_date].tolist()
        if(change_expiry):
            for j in range(1,len(allocation_list)):
                if(j<=18):
                    if(j==1):
                        if(is_third_monday_in_expiry_month(prices_1[0])):
                            profit_perday.append(0)
                        else:
                            print((expiry_price_1-prices_1[j]))
                            profit_perday.append((expiry_price_1-prices_1[j])*allocation_list[j]*100)
                    else:
                        profit = (prices_2[j-1]-prices_1[j])*allocation_list[j]*100
                        profit_perday.append(round(profit,3))
                else:
                    if(j==19):
                        if(is_third_monday_in_expiry_month(prices_1[0])):
                            profit_perday.append(0)
                        else:
                            profit_perday.append((expiry_price_1-prices_1[j])*allocation_list[j]*100)
                    else:
                        profit = (prices_1[j-18]-prices_2[j-19])*allocation_list[j]*100
                        profit_perday.append(round(profit,3))
        else:
            for j in range(1,len(allocation_list)):
                if(j<=18):
                    profit = (prices_2[j]-prices_1[j])*allocation_list[j]*100
                    profit_perday.append(round(profit,3))
                else:
                    profit = (prices_1[j-18]-prices_2[j-18])*allocation_list[j]*100
                    profit_perday.append(round(profit,3))
        profit_perday.append(sum(profit_perday[1:]))
        total_profits.append(profit_perday)
    total_profits_df = pd.DataFrame(total_profits,columns=['Date','FEIcm1', 'FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18','Inverse of FEIcm1', 'Inverse of FEIcm2', 'Inverse of FEIcm3', 'Inverse of FEIcm4', 'Inverse of FEIcm5', 'Inverse of FEIcm6', 'Inverse of FEIcm7', 'Inverse of FEIcm8', 'Inverse of FEIcm9', 'Inverse of FEIcm10', 'Inverse of FEIcm11', 'Inverse of FEIcm12', 'Inverse of FEIcm13', 'Inverse of FEIcm14', 'Inverse of FEIcm15', 'Inverse of FEIcm16', 'Inverse of FEIcm17', 'Inverse of FEIcm18','Profit'])
    total_profits_df.to_csv(f'profit_simple\AntiRoll_{from_date}_{to_date}_{period}.csv')
    colors = ['red' if x < 0 else 'green' for x in total_profits_df['Profit'].tolist()]
    ax1.set_title(f"AntiRoll_{from_date}_{to_date}")
    ax1.bar(range(len(total_profits_df['Profit'].tolist())),total_profits_df['Profit'].tolist(),color=colors)
    ax1.set_xlabel(f"Profit = {sum(total_profits_df['Profit'].tolist())}")
    total_profits.clear()

def roll():
    change_expiry = True
    for i in range(row_number_from_date,row_number_to_date+1):
        profit_perday = []
        prices_1 = prices_df.iloc[i].tolist()
        if((i+period)>=len(prices_df)):
            break
        prices_2 = prices_df.iloc[i+period].tolist()
        profit_perday.append(prices_2[0])
        if((i+period)>len(prices_df)):
            break
        if(is_third_monday_in_expiry_month(prices_2[0])):
            change_expiry =True
        if(is_third_monday_in_expiry_month(prices_df.iloc[i-1].tolist()[0])):
            change_expiry = False
        allocation_list = roll_df.iloc[i-row_number_from_date].tolist()
        if(change_expiry):
            for j in range(1,len(allocation_list)):
                if(j<=18):
                    profit = (prices_2[j]-prices_1[j+1])*allocation_list[j]*100
                    profit_perday.append(round(profit,3))
                else:
                    profit = (prices_1[j-18+1]-prices_2[j-18])*allocation_list[j]*100
                    profit_perday.append(round(profit,3))
        else:
            for j in range(1,len(allocation_list)):
                if(j<=18):
                    profit = (prices_2[j+1]-prices_1[j+1])*allocation_list[j]*100
                    profit_perday.append(round(profit,3))
                else:
                    profit = (prices_1[j-18+1]-prices_2[j-18+1])*allocation_list[j]*100
                    profit_perday.append(round(profit,3))
        profit_perday.append(sum(profit_perday[1:]))
        total_profits.append(profit_perday)
    total_profits_df = pd.DataFrame(total_profits,columns=['Date','FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18','FEIcm19', 'Inverse of FEIcm2', 'Inverse of FEIcm3', 'Inverse of FEIcm4', 'Inverse of FEIcm5', 'Inverse of FEIcm6', 'Inverse of FEIcm7', 'Inverse of FEIcm8', 'Inverse of FEIcm9', 'Inverse of FEIcm10', 'Inverse of FEIcm11', 'Inverse of FEIcm12', 'Inverse of FEIcm13', 'Inverse of FEIcm14', 'Inverse of FEIcm15', 'Inverse of FEIcm16', 'Inverse of FEIcm17', 'Inverse of FEIcm18','Inverse of FEIcm19','Profit'])
    total_profits_df.to_csv(f'profit_simple\Roll_{from_date}_{to_date}_{period}.csv')
    colors = ['red' if x < 0 else 'green' for x in total_profits_df['Profit'].tolist()]
    ax2.set_title(f"Roll_{from_date}_{to_date}")
    ax2.bar(range(len(total_profits_df['Profit'].tolist())),total_profits_df['Profit'].tolist(),color=colors)
    ax2.set_xlabel(f"Profit = {sum(total_profits_df['Profit'].tolist())}")
    total_profits.clear()
roll()
anti_roll()
figure.savefig(f"final_profit\Profit_{from_date}_{to_date}_{period}.pdf")
