#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import os

class Filter:
    """
    Instantiation of this class leads to filtering of the
    original dataset headers with the features identified by the
    concrete autoencoder (plus the output variable, 'stutter').
    Subsequently, the filtered dataset is saved in a new file.

    data_dir: directory containing original data.
    data_file_train: filename of original train data.
    data_file_test: filename of original test data.
    concrete_results_dir: directory containing the file where
    the features selected by the concrete autoencoder is stored.
    concrete_results_file: file containing list of selected 
    features, with which to filter the original data.   
    """
    def __init__(self, data_dir, data_file_train,
                 data_file_test, concrete_results_dir, 
                 concrete_results_file, *args, **kwargs):
        super(Filter, self).__init__(*args, **kwargs)
        self.data_dir = data_dir
        self.data_file_train = data_file_train
        self.data_file_test = data_file_test
        self.concrete_results_dir = concrete_results_dir
        self.concrete_results_file = concrete_results_file

        self.get_train_test_files()
        self.get_concrete_results()
        self.filter()
        self.output_filtered()
    
    def get_original_data_file(self, file):
        data_path = os.join.path(self.data_dir, file)
        return pd.read_csv(data_path)
    
    def get_train_test_files(self):
        self.train_original = self.get_original_data_file(
            self.data_file_train)
        self.test_original = self.get_original_data_file(
            self.data_file_test)
        return self

    def get_concrete_results(self):
        concrete_path = os.join.path(self.concrete_results_dir,
                                     self.concrete_results_file)
        self.concrete_data = pd.read_csv(concrete_path)
        return self

    def filter(self):
        self.selected= self.original_data[self.original_data.head().isin(
            list(self.concrete_data) + 'stutter')]
        return self

    def output_filtered(self):
        os.chdir(self.data_dir)
        self.selected.to_csv('filtered.csv')


    