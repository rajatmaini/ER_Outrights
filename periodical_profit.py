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

period = 3


row_number_from_date = prices_df.loc[prices_df['Date'] == from_date].index[0]
row_number_to_date = prices_df.loc[prices_df['Date'] == to_date].index[0]
def anti_roll():
    c=1
    total_profits = []
    final_positions = []
    for i in range(row_number_from_date,row_number_to_date+1):
        profit_perday = []
        if(c<period):
            prices_1 = prices_df.iloc[i].tolist()
            prices_2 = prices_df.iloc[i+1].tolist()
            profit_perday.append(prices_2[0])
            allocation_list = anti_roll_df.iloc[i-row_number_from_date].tolist()
            if(is_third_monday_in_expiry_month(prices_1[0])):
                profit_perday.append(0)
                for j in range(2,len(allocation_list)):
                    if(j<=18):
                        profit = (prices_2[j-1]-prices_1[j])*allocation_list[j]*100
                        profit_perday.append(round(profit,3))
                    else:
                        if(j==19):
                            profit_perday.append(0)
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
            profit_perday.append(0)
            total_profits.append(profit_perday)
            c+=1
        else:
            prices_0 = prices_df.iloc[i-1].tolist()
            prices_1 = prices_df.iloc[i].tolist()
            prices_2 = prices_df.iloc[i+1].tolist()
            period_profit = []
            total_positions = []
            allocation_list = anti_roll_df.iloc[i-row_number_from_date].tolist()
            for j in range(i-period,i):
                if(len(total_positions)==0):
                    total_positions = anti_roll_df.iloc[j-row_number_from_date+1].tolist()
                else:
                    if(is_third_monday_in_expiry_month(anti_roll_df.iloc[j-row_number_from_date].tolist()[0])):
                        for z in range(2,len(total_positions)):
                            if(z==18):
                                total_positions[z-1] = total_positions[z]
                                total_positions[z] = 0
                            elif(z!=19):    
                                total_positions[z-1] = total_positions[z]
                        total_positions[len(total_positions)-1]=0
                        total_positions = [x+y for x,y in zip(total_positions,anti_roll_df.iloc[j-row_number_from_date+1].tolist())]
                    else:
                        total_positions = [x+y for x,y in zip(total_positions,anti_roll_df.iloc[j-row_number_from_date+1].tolist())]
            if(is_third_monday_in_expiry_month(prices_1[0])):#Period Profit Calculation
                for j in range(1,len(total_positions)):
                    if(j<=18):
                        if(j==1):
                            profit = (prices_1[j]-prices_0[j])*(total_positions[j]-allocation_list[j])*100
                            period_profit.append(round(profit,3))
                        else:
                            profit = (prices_2[j-1]-prices_1[j])*total_positions[j]*100
                            period_profit.append(round(profit,3))
                    else:
                        if(j==19):
                            profit = (prices_0[j]-prices_1[j])*(total_positions[j]-allocation_list[j])*100
                            period_profit.append(round(profit,3))
                        else:
                            profit = (prices_1[j-18]-prices_2[j-19])*total_positions[j]*100
                            period_profit.append(round(profit,3))
                print((period_profit))
            else:
                for j in range(1,len(total_positions)):
                    if(j<=18):
                        profit = (prices_2[j]-prices_1[j])*total_positions[j]*100
                        period_profit.append(round(profit,3))
                    else:
                        profit = (prices_1[j-18]-prices_2[j-18])*total_positions[j]*100
                        period_profit.append(round(profit,3))
            final_positions.append(total_positions)
            profit_perday.append(prices_2[0])
            if(is_third_monday_in_expiry_month(prices_1[0])):
                profit_perday.append(0)
                for j in range(2,len(allocation_list)):
                    if(j<=18):
                        profit = (prices_2[j-1]-prices_1[j])*allocation_list[j]*100
                        profit_perday.append(round(profit,3))
                    else:
                        if(j==19):
                            profit_perday.append(0)
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
            profit_perday.append(sum(period_profit))
            total_profits.append(profit_perday)
    final_positions_df = pd.DataFrame(final_positions,columns=['Date','FEIcm1', 'FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18','Inverse of FEIcm1', 'Inverse of FEIcm2', 'Inverse of FEIcm3', 'Inverse of FEIcm4', 'Inverse of FEIcm5', 'Inverse of FEIcm6', 'Inverse of FEIcm7', 'Inverse of FEIcm8', 'Inverse of FEIcm9', 'Inverse of FEIcm10', 'Inverse of FEIcm11', 'Inverse of FEIcm12', 'Inverse of FEIcm13', 'Inverse of FEIcm14', 'Inverse of FEIcm15', 'Inverse of FEIcm16', 'Inverse of FEIcm17', 'Inverse of FEIcm18'])        
    final_positions_df.to_csv("final_positions_anti_roll.csv")
    total_profits_df = pd.DataFrame(total_profits,columns=['Date','FEIcm1', 'FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18','Inverse of FEIcm1', 'Inverse of FEIcm2', 'Inverse of FEIcm3', 'Inverse of FEIcm4', 'Inverse of FEIcm5', 'Inverse of FEIcm6', 'Inverse of FEIcm7', 'Inverse of FEIcm8', 'Inverse of FEIcm9', 'Inverse of FEIcm10', 'Inverse of FEIcm11', 'Inverse of FEIcm12', 'Inverse of FEIcm13', 'Inverse of FEIcm14', 'Inverse of FEIcm15', 'Inverse of FEIcm16', 'Inverse of FEIcm17', 'Inverse of FEIcm18',"Running",f'{period}_Profit'])
    total_profits_df.to_csv(f'profits\PeriodicAntiRoll_{from_date}_{to_date}_{period}.csv')
    ax1.set_title(f"AntiRoll_{from_date}_{to_date}")
    ax1.plot(total_profits_df['Running'].tolist())
    ax1.set_xlabel(f"Profit = {total_profits_df[f'{period}_Profit'].tolist()[len(total_profits_df['Running'].tolist())-1]}")

def roll():
    total_profits = []
    final_positions = []
    c=1
    for i in range(row_number_from_date,row_number_to_date+1):
        profit_perday = []
        if(c<period):
            prices_1 = prices_df.iloc[i].tolist()
            prices_2 = prices_df.iloc[i+1].tolist()
            profit_perday.append(prices_2[0])
            allocation_list = roll_df.iloc[i-row_number_from_date].tolist()
            if(is_third_monday_in_expiry_month(prices_1[0])):
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
            profit_perday.append(0)
            total_profits.append(profit_perday)
            c+=1
        else:
            prices_1 = prices_df.iloc[i].tolist()
            prices_2 = prices_df.iloc[i+1].tolist()
            period_profit = []
            total_positions = []
            for j in range(i-period,i):
                if(len(total_positions)==0):
                    total_positions = roll_df.iloc[j-row_number_from_date+1].tolist()
                else:
                    if(is_third_monday_in_expiry_month(roll_df.iloc[j-row_number_from_date].tolist()[0])):
                        for z in range(2,len(total_positions)):
                            if(z==18):
                                total_positions[z-1] = total_positions[z]
                                total_positions[z] = 0
                            elif(z!=19):    
                                total_positions[z-1] = total_positions[z]
                        total_positions[len(total_positions)-1]=0
                        total_positions = [x+y for x,y in zip(total_positions,roll_df.iloc[j-row_number_from_date+1].tolist())]
                    else:
                        total_positions = [x+y for x,y in zip(total_positions,roll_df.iloc[j-row_number_from_date+1].tolist())]
            if(is_third_monday_in_expiry_month(prices_1[0])):
                for j in range(1,len(total_positions)):
                    if(j<=18):
                        profit = (prices_2[j]-prices_1[j+1])*total_positions[j]*100
                        period_profit.append(round(profit,3))
                    else:
                        profit = (prices_1[j-18+1]-prices_2[j-18])*total_positions[j]*100
                        period_profit.append(round(profit,3))
            else:
                for j in range(1,len(total_positions)):
                    if(j<=18):
                        profit = (prices_2[j+1]-prices_1[j+1])*total_positions[j]*100
                        period_profit.append(round(profit,3))
                    else:
                        profit = (prices_1[j-18+1]-prices_2[j-18+1])*total_positions[j]*100
                        period_profit.append(round(profit,3))
            final_positions.append(total_positions)
            profit_perday.append(prices_2[0])
            allocation_list = roll_df.iloc[i-row_number_from_date].tolist()
            if(is_third_monday_in_expiry_month(prices_1[0])):
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
            profit_perday.append(sum(period_profit))
            total_profits.append(profit_perday)
    final_positions_df = pd.DataFrame(final_positions,columns=['Date', 'FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18','FEIcm19', 'Inverse of FEIcm2', 'Inverse of FEIcm3', 'Inverse of FEIcm4', 'Inverse of FEIcm5', 'Inverse of FEIcm6', 'Inverse of FEIcm7', 'Inverse of FEIcm8', 'Inverse of FEIcm9', 'Inverse of FEIcm10', 'Inverse of FEIcm11', 'Inverse of FEIcm12', 'Inverse of FEIcm13', 'Inverse of FEIcm14', 'Inverse of FEIcm15', 'Inverse of FEIcm16', 'Inverse of FEIcm17', 'Inverse of FEIcm18','Inverse of FEIcm19'])        
    final_positions_df.to_csv("final_positions_roll.csv")
    total_profits_df = pd.DataFrame(total_profits,columns=['Date', 'FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18','FEIcm19', 'Inverse of FEIcm2', 'Inverse of FEIcm3', 'Inverse of FEIcm4', 'Inverse of FEIcm5', 'Inverse of FEIcm6', 'Inverse of FEIcm7', 'Inverse of FEIcm8', 'Inverse of FEIcm9', 'Inverse of FEIcm10', 'Inverse of FEIcm11', 'Inverse of FEIcm12', 'Inverse of FEIcm13', 'Inverse of FEIcm14', 'Inverse of FEIcm15', 'Inverse of FEIcm16', 'Inverse of FEIcm17', 'Inverse of FEIcm18','Inverse of FEIcm19',"Running",f'{period}_Profit'])
    total_profits_df.to_csv(f'profits\PeriodicRoll_{from_date}_{to_date}_{period}.csv')
    ax2.set_title(f"AntiRoll_{from_date}_{to_date}")
    ax2.plot(total_profits_df['Running'].tolist())
    ax2.set_xlabel(f"Profit = {total_profits_df[f'{period}_Profit'].tolist()[len(total_profits_df['Running'].tolist())-1]}")
roll()
anti_roll()
figure.savefig(f"final_profit_periodic\Profit_{from_date}_{to_date}_{period}.pdf")