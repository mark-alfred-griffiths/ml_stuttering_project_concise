#!/usr/bin/env python
# coding: utf-8
import warnings
from datetime import datetime
import keras_tuner as kt
import numpy as np
import pandas as pd
import tensorflow as tf
from kerastuner_tensorboard_logger import (
    TensorBoardLogger,
    setup_tb
)
from sklearn.metrics import classification_report, confusion_matrix
from best_epochs_widget import *
from create_model import *
from create_output_dense_five_directory import *
from get_summary_stats import *
from reformat_data import *
from standard_scaler import *


class RunTuneGetBestdenseHyperparametersfive:
    def __init__(self, max_epochs, min_delta, batch_size, seed_value, *args, **kwargs):
        super(RunTuneGetBestdenseHyperparametersfive, self).__init__(*args, **kwargs)
        self.max_epochs = max_epochs
        self.min_delta = min_delta
        self.seed_value = seed_value
        self.batch_size = batch_size

        data = InstantiateData(data_dir='/scratch/users/k1754828/DATA/')
        data = DimXNumCats(data)
        data = ConductSklearnStandardScaling(data)
        data = ReformatData(data, batch_size=14000)

        dense_five_dir = CreateDenseFiveDirectory(results_dir='/scratch/users/k1754828/RESULTS/')

        self.xytrain = data.xytrain
        self.xytest = data.xytest
        self.dense = dense_five_dir.dense_tf_five_layer
        self.dense_tf_five_layer_pretraining = dense_five_dir.dense_tf_five_layer_pretraining


        self.dense_tf_five_layer_partial_models = dense_five_dir.dense_tf_five_layer_partial_models
        self.dense_tf_five_layer_tensorboard = dense_five_dir.dense_tf_five_layer_tensorboard
        self.run_tuner()

    def run_tuner(self):
        self.tuner = kt.Hyperband(build_model,
                                  objective=kt.Objective('val_accuracy', direction='max'),
                                  max_epochs=self.max_epochs,
                                  factor=3,
                                  # distribution_strategy=tf.distribute.MirroredStrategy(),
                                  overwrite=False,
                                  directory=self.dense_tf_five_layer_pretraining,
                                  project_name='dense_tf_five_layer_tensorboard',
                                  logger=TensorBoardLogger(metrics=["loss", "accuracy", "val_accuracy", "val_loss", ],
                                                           logdir=self.dense_tf_five_layer_pretraining + "/dense_tf_five_layer_tensorboard/hparams")
                                  )
        setup_tb(self.tuner)
        tensorflow_board = tf.keras.callbacks.TensorBoard(self.dense_tf_five_layer_tensorboard)
        partial_models = tf.keras.callbacks.ModelCheckpoint(filepath=self.dense_tf_five_layer_partial_models +
                                                                     '/model.{epoch:02d}.h5')
        stop_early = tf.keras.callbacks.EarlyStopping(monitor='loss', mode='min', min_delta=self.min_delta,
                                                      patience=5)
        self.tuner.search(self.xytrain, validation_data=self.xytest,
                          callbacks=[stop_early, partial_models, tensorflow_board])
        return self


def run_tuner_get_best_hyperparameters(model_dir, project_name, epochs):
    tuner = kt.Hyperband(build_model, objective='accuracy', max_epochs=epochs, factor=3, directory=model_dir,
                         project_name=project_name)

    best_hps = tuner.get_best_hyperparameters(1)[0]

    return best_hps


def main():
    """
    Runs the following pipeline: 
        - Hyperparameter tuning
        - Get best hyperparameters
        - Train model
        - Get best epoch
        - Evaluate model
        - Save confusion-report class-report and summary statistics
    """
    start_time = datetime.now()
    batch_size = 14000
    epochs = 10000

    data = InstantiateData(data_dir='/scratch/users/k1754828/DATA/')
    data = DimXNumCats(data)
    data = ConductSklearnStandardScaling(data)
    data = ReformatData(data, batch_size=14000)
    SetSeed(1234)
    dense_five_dir = CreateDenseFiveDirectory(results_dir='/scratch/users/k1754828/RESULTS/')

    RunTuneGetBestdenseHyperparametersfive(max_epochs=epochs, min_delta=0.0001, batch_size=batch_size, seed_value=1234)

    best_hps=run_tuner_get_best_hyperparameters(model_dir=dense_five_dir.dense_tf_five_layer_pretraining, project_name='/dense_tf_five_layer_tensorboard', epochs=10000)

    epoch_training_model_path = Path(str(dense_five_dir.dense_tf_five_layer_epoch_select_model + '/dense_tf_five_layer_epoch_training_model'))
    if epoch_training_model_path.exists():
        model = tf.keras.models.load_model(str(dense_five_dir.dense_tf_five_layer_epoch_select_model + '/dense_tf_five_layer_epoch_training_model'))
    else:
        model = kt.hypermodel.build(best_hps)
        history = model.fit(data.xtest, validation_data=(data.xtest), epochs=10000, batch_size=14000)
        val_acc_per_epoch = history.history['val_accuracy']
        best_epoch = val_acc_per_epoch.index(max(val_acc_per_epoch)) + 1
        model.save(str(dense_five_dir.dense_tf_five_layer_epoch_select_model + '/dense_tf_five_layer_epoch_training_model'))
        output_best_epoch(dense_five_dir, best_epoch)

    epoch_training_model_path = Path(str(dense_five_dir.dense_tf_five_layer_final_model + '/dense_tf_five_layer_final_model'))
    if epoch_training_model_path.exists():
        model = tf.keras.models.load_model(str(dense_five_dir.dense_tf_five_layer_final_model + '/dense_tf_five_layer_final_model'))
        best_epoch = get_best_epoch(dense_five_dir)
    else:
        model = kt.hypermodel.build(best_hps)
        # Retrain the model
        model.fit(data.xytrain, validation_data=(data.xytest), epochs=best_epoch)
        model.save(str(dense_five_dir.dense_tf_five_layer_final_model + '/dense_tf_five_layer_final_model'))

    test_results = model.evaluate(data.xtest, data.ytest, verbose=1)
    stutter_preds = np.array(model.predict(data.xtest))
    num_classes = len(np.unique(np.argmax(stutter_preds, axis=1)))

    class_report = classification_report(np.argmax(data.ytest, axis=1), np.argmax(stutter_preds, axis=1))
    class_report = pd.DataFrame([class_report]).transpose()
    conf_mat = confusion_matrix(np.argmax(data.ytest, axis=1), np.argmax(stutter_preds, axis=1))
    conf_mat = pd.DataFrame(conf_mat)
    test_results = pd.DataFrame([test_results])
    test_results.columns = ['Loss', 'Accuracy']

    [mse, bic, aic] = get_mse_bic_aic(np.argmax(data.ytest, axis=1), np.argmax(stutter_preds, axis=1), model)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        roc_auc = compute_roc_and_auc(np.argmax(data.ytest, axis=1), np.argmax(stutter_preds, axis=1), num_classes)

    summary_stats = pd.concat([roc_auc, mse, bic, aic], axis=1).T.reset_index()

    best_hps_vals = pd.DataFrame.from_dict(best_hps.values())
    os.chdir(dense_five_dir.dense_tf_five_layer_results)
    test_results.to('test_results.csv', index=False)
    summary_stats.to_csv('summary_stats.csv', index=False)
    pd.DataFrame(conf_mat).to_csv('conf_mat.csv', index=False)
    pd.DataFrame(class_report).to_csv('class_report.csv', index=False)
    best_hps_vals.to_csv('best_hps_vals.csv', index=False)

    time_delta = datetime.now() - start_time

    exit_message = 'dense five HYPERBAND RAN SUCCESSFULLY IN: ' + str(time_delta)
    sys.exit(exit_message)


# RUN ALL
if __name__ == "__main__":
    main()
