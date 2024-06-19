# -*- coding: utf-8 -*-
# @Time    : 05/06/2024
# @Author  : Ing. Jorge Lara
# @Email   : jlara@iee.unsj.edu.ar
# @File    : data_preprocessing.py
# @Software: PyCharm

import os
import glob
import pandas as pd
import numpy as np
from .utils import add_time_features
from .prepare_data import get_scenarios_for_time_features
from .BBDD.load_example import example


def _user_id(data):
    return data['Unnamed: 1'][1]


def _clean_file(df):
    df = df.drop([0, 1, 2, 3, 4, 5, 6])
    df = df.dropna(how='all', axis=1)
    df.columns = list(df.iloc[:1].values[0])
    df = df.drop([df.index[0]], axis=0)
    df.set_index(df.columns[0], inplace=True)
    df = df.loc[pd.notnull(df.index)]
    df = df[[x for x in list(df.columns) if str(x) != 'nan']]
    df['W'] = df['Wh'] / 0.25
    return df[list(df.columns)[-2:]]


class scenarios:

    @staticmethod
    def dictionary():
        """
        This function returns a dictionary with the following keys

        'seasons': None,  # ['Summer', 'Fall', 'Winter', 'Spring']
        'month': None,  # ['January' 'February' 'March' 'April' 'May' 'June' 'July' 'August', 'September' 'October' 'November' 'December']
        'year': None,  # [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
        'day_name': None,  # ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        'day_type': None,  # ['working', 'non-working']
        'date': None  # ['2013-08-31', '2014-02-28']

        :return: dict_sce
        """
        dict_sce = {
            'seasons': None,  # ['Summer', 'Fall', 'Winter', 'Spring']
            'month': None,  # ['January' 'February' 'March' 'April' 'May' 'June' 'July' 'August', 'September' 'October' 'November' 'December']
            'year': None,  # [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
            'day_name': None,  # ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            'day_type': None,  # ['working', 'non-working']
            'date': None  # ['2013-08-31', '2014-02-28']
        }
        return dict_sce
    def multiple_users(
            self,
            file_path: str = None,
            index_col: int = 0,
            parse_dates: bool = True,
            dict_scenario: dict = None,
            id_col_users:  str = 'nroserie',
            variable: str = 'kW',
    ):
        """
        This function reads a csv file with the following columns:
        :param file_path: path to the csv file
        :param index_col: index column
        :param parse_dates: boolean to parse dates
        :param dict_scenario: dictionary with the following keys
        :param id_col_users: id column for users
        :param variable: variable to be analyzed
        :return:
        """
        if file_path is None:
            data = example()
        else:
            data = pd.read_csv(
                file_path,
                index_col=index_col,
                parse_dates=parse_dates
            )

        data = pd.pivot_table(
            data=data,
            index=data.index,
            columns=id_col_users,
            values=variable
        )
        data.index.name = 'index'
        if data.isnull().sum().sum() > 0:
            moving_window_replace(data.values, n_days=7)
        data = add_time_features(data)
        if dict_scenario is None:
            scenarios = get_scenarios_for_time_features(
                data,
                seasons=True,
                month=True,
                day_name=True,
                day_type=True
            )
            return scenarios
        else:
            for key, value in dict_scenario.items():
                if value is None:
                    dict_scenario[key] = list(data[key].unique())
            if len(dict_scenario['date']) > 2:
                data_filter = data[
                    (data.seasons.isin(dict_scenario['seasons'])) &
                    (data.month.isin(dict_scenario['month'])) &
                    (data.year.isin(dict_scenario['year'])) &
                    (data.day_name.isin(dict_scenario['day_name'])) &
                    (data.day_type.isin(dict_scenario['day_type']))
                    ]
            elif len(dict_scenario['date']) == 2:
                data_filter = data[
                    (data.seasons.isin(dict_scenario['seasons'])) &
                    (data.month.isin(dict_scenario['month'])) &
                    (data.year.isin(dict_scenario['year'])) &
                    (data.day_name.isin(dict_scenario['day_name'])) &
                    (data.day_type.isin(dict_scenario['day_type'])) &
                    (data.date >= dict_scenario['date'][0]) &
                    (data.date <= dict_scenario['date'][1])
                    ]
            elif len(dict_scenario['date']) == 1:
                data_filter = data[
                    (data.seasons.isin(dict_scenario['seasons'])) &
                    (data.month.isin(dict_scenario['month'])) &
                    (data.year.isin(dict_scenario['year'])) &
                    (data.day_name.isin(dict_scenario['day_name'])) &
                    (data.day_type.isin(dict_scenario['day_type'])) &
                    (data.date >= dict_scenario['date'][0])
                    ]
            if data_filter.empty:
                print('Modify the scenario filtering dictionary')
                return None
            else:
                data_filter
                return data_filter

    def single_user(
            self,
            file_path,
            dict_scenario: dict = None,
            id_user: str = None,
            only_df: bool = None,
            index_col: int = 0,
            parse_dates: bool = True

    ):
        """
        This function reads a csv file with the following columns
        :param file_path: path to the csv file
        :param dict_scenario: dictionary with the following keys
        :param id_user: id column for user to select
        :param only_df: boolean to return only the dataframe
        :param index_col: number of the index column
        :param parse_dates: boolean to parse dates
        :return:
        """
        if dict_scenario is not None:
            only_df = False
        data = pd.read_csv(
            file_path,
            index_col=index_col,
            parse_dates=parse_dates
        )
        if data.isnull().sum().sum() > 0:
            moving_window_replace(data.values, n_days=7)
        if id_user is None:
            col_init = list(data.columns)[0]
            data = data[[col_init]]
        else:
            #col_init = id_user
            data = data[[id_user]]
        data = add_time_features(data)
        if dict_scenario is None:
            if only_df:
                return data
            else:
                return get_scenarios_for_time_features(
                    data,
                    seasons=True,
                    month=True,
                    day_name=True,
                    day_type=True
                )
        else:
            for key, value in dict_scenario.items():
                if value is None:
                    dict_scenario[key] = list(data[key].unique())
            data_filter = data[
                (data.seasons.isin(dict_scenario['seasons'])) &
                (data.month.isin(dict_scenario['month'])) &
                (data.year.isin(dict_scenario['year'])) &
                (data.day_name.isin(dict_scenario['day_name'])) &
                (data.day_type.isin(dict_scenario['day_type']))
            ]
            if data_filter.empty:
                print('Modify the scenario filtering dictionary')
                return None
            else:
                data_filter
                return data_filter

    def filter_scenario(self):
        pass


def moving_window_replace(
        data: np.array = None,
        res_min: int = 15,
        n_days: int = None,
        previous: bool = None,
        back: bool = None
):
    """
    This function replaces NaN values in a time series using a moving window
    :param data: data to be analyzed in a numpy array
    :param res_min: time resolution in minutes
    :param n_days: number of days to be considered in the moving window
    :param previous: boolean to consider the previous values
    :param back: boolean to consider the back values
    :return:
    """
    if previous is None and back is None:
        previous = True
    window = (24 * 60) / res_min
    if n_days is not None:
        window = window * n_days
    n = 0
    window = int(window)
    while len(data[np.isnan(data)]) > 0:
        print(f'iter:{n}, n_NaN:{len(data[np.isnan(data)])}')
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if np.isnan(data[row, col]):
                    if previous:
                        try:
                            data[row, col] = data[row - window, col]
                        except IndexError:
                            try:
                                data[row, col] = data[row + window, col]
                            except IndexError:
                                pass
                    if back:
                        try:
                            data[row, col] = data[row + window, col]
                        except IndexError:
                            try:
                                data[row, col] = data[row - window, col]
                            except IndexError:
                                pass
        n += 1


def moving_window_mean(
        data: np.array = None,
        n_hours: int = None,
        res_min: int = None,
        n_past: bool = None,
        n_future: bool = None,
):
    """
    This function replaces NaN values in a time series using a moving window
    :param data: data to be analyzed in a numpy array
    :param n_hours: number of hours to be considered in the moving window
    :param res_min: resolution in minutes
    :param n_past: boolean to consider the past values
    :param n_future: boolean to consider the future values
    :return:
    """
    aux = 0
    if n_hours is None:
        n = 1
        n_hours = n * 60
    while len(data[np.isnan(data)]) > 0:
        print(f'iter:{aux}, n_NaN:{len(data[np.isnan(data)])}')
        if n_past is None and n_future is None and res_min is not None:
            n_past, n_future = n_hours / res_min, n_hours / res_min
        elif n_past is None and n_future is None and res_min is None:
            n_past, n_future = 4, 4
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if np.isnan(data[row, col]):
                    data[row, col] = np.concatenate(
                        (
                            data[row - n_past: row, col],
                            data[row: row + n_future, col]
                        )
                    ).mean()
                    if np.isnan(data[row, col]):
                        data[row, col] = data[row - n_past: row, col].mean()
                        if np.isnan(data[row, col]):
                            data[row, col] = data[row: row + n_future, col].mean()
        aux += 1
