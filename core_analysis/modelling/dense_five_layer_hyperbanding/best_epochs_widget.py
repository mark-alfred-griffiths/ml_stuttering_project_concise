#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import os


def output_best_epoch(dense_five_dir, best_epoch):
    os.chdir(dense_five_dir.dense_tf_five_layer_results)
    best_epoch_df = pd.DataFrane(np.array([best_epoch]), columns=['best_epochs'])
    best_epoch_df.to_csv('best_epochs.csv')


def get_best_epoch(dense_five_dir):
    os.chdir(dense_five_dir)
    return pd.DataFrame.read_csv('best_epochs.csv')['best_epooch'][0]