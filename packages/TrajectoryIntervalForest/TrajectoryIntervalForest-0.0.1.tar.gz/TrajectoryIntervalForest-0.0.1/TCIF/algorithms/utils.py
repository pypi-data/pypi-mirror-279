import pandas as pd
from tqdm.auto import tqdm


def data_split(df: pd.DataFrame, tid_list, verbose=False, tid_name="tid", target_name="class", lat_name="c1", lon_name="c2",
               time_name="t"):
    id = []
    lat = []
    lon = []
    time = []
    classe = []

    other_signals = df.drop(columns=[tid_name, target_name, lat_name, lon_name, time_name]).columns
    others = []

    for _id, _classe in tqdm(df[df.tid.isin(tid_list)][[tid_name, target_name]].groupby(by=[tid_name, target_name])
                                     .max().reset_index().values, disable=not verbose, desc="Preparing data", position=0, leave=False):
        df_result = df[df.tid == _id]
        id.append(_id)
        classe.append(_classe)

        _lat = []
        _lon = []
        _time = []
        _others = []

        lat.append(df_result[lat_name].values)
        lon.append(df_result[lon_name].values)
        time.append(df_result[time_name].values)
        others.append(df_result[other_signals].values)

    return id, classe, lat, lon, time, others

def prepare_set(time_train, lat_train, lon_train, others_train):
    res = []
    for _time, _lat, _lon, _others in zip(time_train, lat_train, lon_train, others_train):
        res.append(tuple([_time, _lat, _lon] + [[x[i] for x in _others] for i in range(len(_others[0]))]))

    return res