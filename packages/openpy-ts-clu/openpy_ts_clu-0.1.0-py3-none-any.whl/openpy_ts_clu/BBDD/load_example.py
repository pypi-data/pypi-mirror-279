# -*- coding: utf-8 -*-
# @Time    : 05/06/2023
# @Author  : Ing. Jorge Lara
# @Email   : jlara@iee.unsj.edu.ar
# @File    : load_example.py
# @Software: PyCharm

import os
import pathlib
import pandas as pd


def example():
    script_path = os.path.dirname(os.path.abspath(__file__))
    path_aux = pathlib.Path(script_path).joinpath("dataset_imputation_30min.csv")
    return pd.read_csv(
        path_aux,
        index_col=0,
        parse_dates=True
    )