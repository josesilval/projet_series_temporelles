#### imports ####
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    #### read data ####
    df = pd.read_csv("DS_IPC_PRINC_CSV_FR/DS_IPC_PRINC_data.csv", sep=";")

    #### select data ####
    data = df[
        (df['IND_TYPE'] == 'M_VAR') # monthly variation
        & (df['IDX_TYPE'] == 'CPI') # cpi
        & (df['PRODUCT_GROUP'] == "4035") # ensemble s/seasonality
    ]

    #### date parsing ####
    data['TIME_PERIOD'] = pd.to_datetime(data['TIME_PERIOD'])
    data = data.sort_values('TIME_PERIOD')

    #### time series ####
    series = data[['TIME_PERIOD', 'OBS_VALUE']]

    #### column names ####
    series = series.rename(columns=
                {'TIME_PERIOD': 'date',
                'OBS_VALUE': 'var_ipc'})

    #### save data ####
    series.to_csv('var_ipc.csv', index=False)
