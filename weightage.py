import pandas as pd
import pypfopt
import covariance
file_path = 'ER_Outrights_daily.csv'

df = pd.read_csv(file_path)
from_date = "2023-10-02"
to_date = "2023-12-01"
row_number_from_date = df.loc[df['Date'] == from_date].index[0]+1
row_number_to_date = df.loc[df['Date'] == to_date].index[0]+1
list_of_weights= []
dates = []
def roll():
    for i in range(row_number_from_date,row_number_to_date+1):
        prices = df.iloc[i-1].tolist()
        dates.append(prices[0])
        cov = covariance.return_cov_matrix_roll(i-1)
        mean_returns = []
        for i in range(2,len(prices)-1):
            mean_returns.append(round(prices[i-1]-prices[i],3))
        print(mean_returns)
        ef = pypfopt.EfficientFrontier(mean_returns,cov,weight_bounds=(-1,1))
        weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()
        weights_list = []
        for key, value in cleaned_weights.items():
            weights_list.append(round(value,2))
        ef.portfolio_performance(verbose=True)
        list_of_weights.append(cleaned_weights)
        print(sum(weights_list))
data = []
def anti_roll():
    for i in range(row_number_from_date,row_number_to_date+1):
        prices = df.iloc[i-1].tolist()
        dates.append(prices[0])
        cov = covariance.return_cov_matrix_antiroll(i-1)
        mean_returns = []
        for i in range(1,len(prices)-2):
            mean_returns.append(round(prices[i+1]-prices[i],3))
        print(mean_returns)
        ef = pypfopt.CLA(expected_returns=mean_returns,cov_matrix=cov,weight_bounds=(-1,1))
        ef.max_sharpe()
        cleaned_weights = ef.clean_weights()
        weights_list = []
        for key, value in cleaned_weights.items():
            weights_list.append(round(value,2))
        ef.portfolio_performance(verbose=True)
        list_of_weights.append(cleaned_weights)
        print(sum(weights_list))
anti_roll()
data_df = pd.DataFrame(data)
data_df.to_csv("returns_antiroll.csv",index=False,header=False)
columns = list(list_of_weights[0].keys())
allocation_data_frame = pd.DataFrame(columns=columns)
for data_dict in list_of_weights:
    allocation_data_frame = allocation_data_frame.append(data_dict,ignore_index=True)
allocation_data_frame.index = dates
allocation_data_frame = allocation_data_frame.round(2)
allocation_data_frame.to_csv("AllocationData.csv")