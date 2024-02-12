import pandas as pd
import pypfopt
import covariance,customcovarinace
file_path = 'ER_Outrights_daily.csv'

df = pd.read_csv(file_path)
from_date = "2020-11-02"
to_date = "2021-04-01"
row_number_from_date = df.loc[df['Date'] == from_date].index[0]+1
row_number_to_date = df.loc[df['Date'] == to_date].index[0]+1
list_of_weights= []
dates = []
data = []
def roll():
    for i in range(row_number_from_date,row_number_to_date+1):
        prices = df.iloc[i-1].tolist()
        dates.append(prices[0])
        cov = customcovarinace.customcovarinace_roll(i)
        mean_returns = []
        for i in range(2,len(prices)-1):
            mean_returns.append(round(prices[i-1]-prices[i],3))
        mean_returns.extend([-x for x in mean_returns])
        data.append(mean_returns)
        ef = pypfopt.EfficientFrontier(mean_returns,cov,weight_bounds=(0,1))
        ef.add_objective(pypfopt.objective_functions.L2_reg, gamma=1)
        weights = ef.max_sharpe()
        # cleaned_weights = ef.clean_weights()
        weights_list = []
        for key, value in weights.items():
            weights_list.append(round(value,2))
        ef.portfolio_performance(verbose=True)
        list_of_weights.append(weights)
        print(sum(weights_list))
    data_df = pd.DataFrame(data)
    data_df.to_csv(f"returns_roll_{from_date}_{to_date}.csv",index=dates,header=False)
    columns = list(list_of_weights[0].keys())
    allocation_data_frame = pd.DataFrame(columns=columns)
    for data_dict in list_of_weights:
        allocation_data_frame = allocation_data_frame.append(data_dict,ignore_index=True)
    allocation_data_frame.index = dates
    allocation_data_frame = allocation_data_frame.round(2)
    allocation_data_frame.to_csv(f'calculation\AllocationDataRoll_{from_date}_{to_date}.csv')
def anti_roll():
    data.clear()
    list_of_weights.clear()
    dates.clear()
    for i in range(row_number_from_date,row_number_to_date+1):
        prices = df.iloc[i-1].tolist()
        dates.append(prices[0])
        cov = customcovarinace.customcovarinace(i)
        mean_returns = []
        for i in range(1,len(prices)-2):
            mean_returns.append(round(prices[i+1]-prices[i],3))
        mean_returns.extend([-x for x in mean_returns])
        data.append(mean_returns)
        ef = pypfopt.EfficientFrontier(expected_returns=mean_returns,cov_matrix=cov,weight_bounds=(0,1))
        ef.add_objective(pypfopt.objective_functions.L2_reg)
        weights= ef.max_sharpe()
        # cleaned_weights = ef.clean_weights()
        weights_list = []
        for key, value in weights.items():
            weights_list.append(round(value,2))
        ef.portfolio_performance(verbose=True)
        list_of_weights.append(weights)
        print(sum(weights_list))
    data_df = pd.DataFrame(data)
    data_df.to_csv(f"returns_anti_roll_{from_date}_{to_date}.csv",index=dates,header=False)
    columns = list(list_of_weights[0].keys())
    allocation_data_frame = pd.DataFrame(columns=columns)
    for data_dict in list_of_weights:
        allocation_data_frame = allocation_data_frame.append(data_dict,ignore_index=True)
    allocation_data_frame.index = dates
    allocation_data_frame = allocation_data_frame.round(2)
    allocation_data_frame.to_csv(f'calculation\AllocationDataAntiRoll_{from_date}_{to_date}.csv')
roll()
anti_roll()
