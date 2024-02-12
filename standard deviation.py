import pandas as pd
from datetime import datetime, timedelta
import statistics
import decimal

file_path = 'ER_Outrights_daily.csv'

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

df = pd.read_csv(file_path)
final_dev_data  = [] # Final Calculated Data
df1 = df.values
for i in range(0,len(df1)):
    row = [] #Each Date Data
    row.append(df1[i][0]) # Date
    if(i-29<0):
        row.append(20*[0])
    else:
        for j in range(1,len(df1[i])):
            data =  [] #Price Data for Standard Deviation
            change_expiry = False
            end_contract = False
            for z in range(i,i-30,-1):
                if(is_third_monday_in_expiry_month(df1[z][0]) and len(data)!=0):
                    change_expiry = True
                if(change_expiry):
                    if((j+1)==len(df1[i])):
                        end_contract = True
                        break
                    data.append(df1[z][j+1])
                else:
                    data.append(df1[z][j])
            if(end_contract):
                row.append("INF") #For last contract
            else:
                row.append(statistics.stdev(data)) # Add standard deviation for each column
    final_dev_data.append(row)   # Adding Each Row Data to Final Data
final_df = pd.DataFrame(final_dev_data)
final_df.to_csv("test.csv",index=False,header=['Date','FEIcm1', 'FEIcm2', 'FEIcm3', 'FEIcm4', 'FEIcm5', 'FEIcm6', 'FEIcm7', 'FEIcm8', 'FEIcm9', 'FEIcm10', 'FEIcm11', 'FEIcm12', 'FEIcm13', 'FEIcm14', 'FEIcm15', 'FEIcm16', 'FEIcm17', 'FEIcm18', 'FEIcm19', 'FEIcm20']
)