import pandas as pd
from datetime import datetime,timedelta
import pypfopt

file_path = "ER_Outrights_daily.csv"

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

def return_cov_matrix_roll(row):
    df = pd.read_csv(file_path)
    prices = df.values
    sample_30_days = []
    for i in range(row,len(prices)):
        change_expiry = False
        for z in range(i,i-30,-1):
            row = []
            row.append(prices[z][0])
            for j in range(2,len(prices[i])-1):
                if(is_third_monday_in_expiry_month(prices[z][0]) and len(sample_30_days)>0):
                    print(prices[z][0])
                    change_expiry = True
                if(change_expiry):
                    row.append(prices[z][j+1])
                else:
                    row.append(prices[z][j])
            sample_30_days.append(row)
        break
    print(sample_30_days[0])
    dates = []
    for i in range(len(sample_30_days)):
        dates.append(sample_30_days[i][0]) 
    thirty_days_df = pd.DataFrame(sample_30_days,columns=['Date','FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18', 'FEIcm19'])
    thirty_days_df.drop('Date',axis=1,inplace=True)
    cov = pypfopt.risk_models.risk_matrix(thirty_days_df,"sample_cov")
    cov.to_csv("covariance_outrights.csv")
    return cov

def return_cov_matrix_antiroll(row):
    df = pd.read_csv(file_path)
    prices = df.values
    sample_30_days = []
    for i in range(row,len(prices)):
        change_expiry = False
        for z in range(i,i-30,-1):
            row = []
            row.append(prices[z][0])
            for j in range(1,len(prices[i])-2):
                    if(is_third_monday_in_expiry_month(prices[z][0]) and len(sample_30_days)>0):
                        change_expiry = True
                    if(change_expiry):
                        row.append(prices[z][j+1])
                    else:
                        row.append(prices[z][j])
            sample_30_days.append(row)
        break
    print(sample_30_days[0])
    dates = []
    for i in range(len(sample_30_days)):
        dates.append(sample_30_days[i][0]) 
    thirty_days_df = pd.DataFrame(sample_30_days,columns=['Date','FEIcm1', 'FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18'])
    thirty_days_df.drop('Date',axis=1,inplace=True)
    cov = pypfopt.risk_models.risk_matrix(thirty_days_df,"sample_cov")
    return cov