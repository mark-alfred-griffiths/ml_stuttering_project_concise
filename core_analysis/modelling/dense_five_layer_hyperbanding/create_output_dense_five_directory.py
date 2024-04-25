#!/usr/bin/env python
# coding: utf-8
import os
from pathlib import Path


class CreateDenseFiveDirectory:
    def __init__(self, results_dir, *args, **kwargs):
        super(CreateDenseFiveDirectory, self).__init__(*args, **kwargs)
        self.results_dir = results_dir
        self.dense = self.propagate_dir(results_dir, 'dense_tf')
        self.dense_tf_five_layer = self.propagate_dir(self.dense, 'dense_tf_five_layer')
        self.dense_tf_five_layer_results = self.propagate_dir(self.dense_tf_five_layer, 'dense_tf_five_layer_results')
        self.dense_tf_five_layer_final_model = self.propagate_dir(self.dense_tf_five_layer, 'dense_tf_five_layer_final_model')
        self.dense_tf_five_layer_epoch_select_model = self.propagate_dir(self.dense_tf_five_layer, 'dense_tf_five_layer_epoch_select_model')
        self.dense_tf_five_layer_pretraining = self.propagate_dir(self.dense_tf_five_layer, 'dense_tf_five_layer_pretraining')
        self.dense_tf_five_layer_tensorboard = self.propagate_dir(self.dense_tf_five_layer_pretraining,
                                                                    'dense_tf_five_layer_tensorboard')
        self.dense_tf_five_layer_partial_models = self.propagate_dir(self.dense_tf_five_layer_pretraining,
                                                                   'dense_tf_five_layer_partial_models')


    def propagate_dir(self, old_dir, sub_dir):
        new_dir = Path.home().joinpath(old_dir, str(sub_dir))
        if new_dir.exists():
            pass
        else:
            os.makedirs(new_dir)
        new_dir = str(new_dir)
        return new_dir

