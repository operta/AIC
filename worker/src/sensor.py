from pandas import read_csv
import torch
import numpy as np
import pathlib

STREAM_SAMPLE_WINDOW_K = 100


def load_sensor_data(worker_id):
    df = read_csv(str(pathlib.Path(__file__).parent.absolute()) + '/data/air_pollution_austria_2016_20stations_all.csv')

    number_of_stations = len(df['station_id'].unique())
    if worker_id > number_of_stations:
        df = df[df['station_id'] == 1]
    else:
        df = df[df['station_id'] == worker_id]

    return df.sample(n=STREAM_SAMPLE_WINDOW_K, replace=True)


def convert_data_to_tensor(data):
    y = data['SO2']
    X = data.drop(['station_id', 'SO2'], axis=1)
    return torch.tensor(np.array(X.values),dtype=torch.float32),\
           torch.tensor(np.array(y.values),dtype=torch.float32)

