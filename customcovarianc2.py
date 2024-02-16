import pandas as pd
import pypfopt
from datetime import datetime,timedelta
import numpy
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

prices_df = pd.read_csv(file_path)
def customcovarinace(row):
    total_returns = []
    dates = []
    change_expiry = False
    for i in range(row,row-30,-1):
        prices = prices_df.iloc[i-1].tolist()
        row = [prices[0]]
        if(is_third_monday_in_expiry_month(prices[0]) and len(total_returns)>0):
            change_expiry = True
        for j in range(1,len(prices)-2):
            if(change_expiry):
                row.append(prices[j+1])
            else:
                row.append(prices[j])
        total_returns.append(row)
    print(total_returns[0])
    total_returns_df = pd.DataFrame(total_returns,columns=['Date','FEIcm1', 'FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18']
    )
    total_returns_df.drop("Date",axis=1,inplace=True)
    cov = pypfopt.risk_models.risk_matrix(total_returns_df,"sample_cov",returns_data=True,frequency=1)
    cov_matrix = cov.values.tolist()
    cov_matrix_copy = []
    for i in range(len(cov_matrix)):
        row = list(cov_matrix[i])
        row.extend([-x for x in row])
        cov_matrix_copy.append(row)
    test = []
    for i in range(len(cov_matrix_copy),2*len(cov_matrix_copy)):
        row = cov_matrix_copy[i-len(cov_matrix_copy)]
        row = [-x for x in row]
        test.append(row)
    cov_matrix_copy.extend(test)
    cov_matrix_copy_df = pd.DataFrame(cov_matrix_copy,index=['FEIcm1', 'FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18','Inverse of FEIcm1', 'Inverse of FEIcm2', 'Inverse of FEIcm3', 'Inverse of FEIcm4', 'Inverse of FEIcm5', 'Inverse of FEIcm6', 'Inverse of FEIcm7', 'Inverse of FEIcm8', 'Inverse of FEIcm9', 'Inverse of FEIcm10', 'Inverse of FEIcm11', 'Inverse of FEIcm12', 'Inverse of FEIcm13', 'Inverse of FEIcm14', 'Inverse of FEIcm15', 'Inverse of FEIcm16', 'Inverse of FEIcm17', 'Inverse of FEIcm18']
,columns=['FEIcm1', 'FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18','Inverse of FEIcm1', 'Inverse of FEIcm2', 'Inverse of FEIcm3', 'Inverse of FEIcm4', 'Inverse of FEIcm5', 'Inverse of FEIcm6', 'Inverse of FEIcm7', 'Inverse of FEIcm8', 'Inverse of FEIcm9', 'Inverse of FEIcm10', 'Inverse of FEIcm11', 'Inverse of FEIcm12', 'Inverse of FEIcm13', 'Inverse of FEIcm14', 'Inverse of FEIcm15', 'Inverse of FEIcm16', 'Inverse of FEIcm17', 'Inverse of FEIcm18'])
    cov_matrix_copy_df.to_csv("test_custom_cov.csv")
    return cov_matrix_copy_df

def customcovarinace_roll(row):
    total_returns = []
    change_expiry = False
    for i in range(row,row-30,-1):
        prices = prices_df.iloc[i-1].tolist()
        row = [prices[0]]
        if(is_third_monday_in_expiry_month(prices[0]) and len(total_returns)>0):
            change_expiry = True
        for j in range(2,len(prices)-1):
            if(change_expiry):
                row.append(prices[j+1])
            else:
                row.append(prices[j])
        total_returns.append(row)
    print(total_returns[0])
    total_returns_df = pd.DataFrame(total_returns,columns=['Date','FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17','FEIcm18','FEIcm19']
    )
    total_returns_df.drop('Date',axis=1,inplace=True)
    cov = pypfopt.risk_models.risk_matrix(total_returns_df,"sample_cov",returns_data=True,frequency=1)
    cov_matrix = cov.values.tolist()
    cov_matrix_copy = []
    for i in range(len(cov_matrix)):
        row = list(cov_matrix[i])
        row.extend([-x for x in row])
        cov_matrix_copy.append(row)
    test = []
    for i in range(len(cov_matrix_copy),2*len(cov_matrix_copy)):
        row = cov_matrix_copy[i-len(cov_matrix_copy)]
        row = [-x for x in row]
        test.append(row)
    cov_matrix_copy.extend(test)
    cov_matrix_copy_df = pd.DataFrame(cov_matrix_copy,index=['FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18','FEIcm19','Inverse of FEIcm2', 'Inverse of FEIcm3', 'Inverse of FEIcm4', 'Inverse of FEIcm5', 'Inverse of FEIcm6', 'Inverse of FEIcm7', 'Inverse of FEIcm8', 'Inverse of FEIcm9', 'Inverse of FEIcm10', 'Inverse of FEIcm11', 'Inverse of FEIcm12', 'Inverse of FEIcm13', 'Inverse of FEIcm14', 'Inverse of FEIcm15', 'Inverse of FEIcm16', 'Inverse of FEIcm17', 'Inverse of FEIcm18','Inverse of FEIcm19']
,columns=['FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18','FEIcm19','Inverse of FEIcm2', 'Inverse of FEIcm3', 'Inverse of FEIcm4', 'Inverse of FEIcm5', 'Inverse of FEIcm6', 'Inverse of FEIcm7', 'Inverse of FEIcm8', 'Inverse of FEIcm9', 'Inverse of FEIcm10', 'Inverse of FEIcm11', 'Inverse of FEIcm12', 'Inverse of FEIcm13', 'Inverse of FEIcm14', 'Inverse of FEIcm15', 'Inverse of FEIcm16', 'Inverse of FEIcm17', 'Inverse of FEIcm18','Inverse of FEIcm19'])
    cov_matrix_copy_df.to_csv("test_custom_cov.csv")
    return cov_matrix_copy_df
