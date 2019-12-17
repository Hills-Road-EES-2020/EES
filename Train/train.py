import argparse
import datetime
from Model import TheBox
import numpy as np
import os
import random
import sklearn.model_selection as ms
import tensorflow as tf
import time

def _get_img(filename, label):
    img = tf.io.read_file(filename)
    img = tf.image.decode_jpeg(img)
    img = (tf.cast(img, tf.float32)/127.5) - 1
    img = tf.image.resize(img, (HEIGHT, WIDTH))
    return img, label

def get_data(folder):
    hot_files = [os.path.join(folder,CLASS_0,f) for f in os.listdir(os.path.join(folder,CLASS_0))]
    random.shuffle(hot_files)
    hot_labels = [0 for x in range(len(hot_files))]

    not_files = [os.path.join(folder,CLASS_1,f) for f in os.listdir(os.path.join(folder,CLASS_1))]
    random.shuffle(not_files)
    not_labels = [1 for x in range(len(not_files))]

    filenames = hot_files+not_files
    labels = hot_labels+not_labels

    train_filenames, val_filenames, train_labels, val_labels = ms.train_test_split(
                            filenames, labels, train_size=0.8)
    train_data = tf.data.Dataset.from_tensor_slices(
        (tf.constant(train_filenames), tf.constant(train_labels)))
    val_data = tf.data.Dataset.from_tensor_slices(
        (tf.constant(val_filenames), tf.constant(val_labels)))
    train_data = (train_data.map(_get_img).shuffle(buffer_size=1000).batch(BATCH_SIZE))
    val_data = (val_data.map(_get_img).shuffle(buffer_size=1000).batch(BATCH_SIZE))
    return train_data, val_data