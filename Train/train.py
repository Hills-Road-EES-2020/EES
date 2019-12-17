import argparse
import datetime
from Model import thebox
import numpy as np
import os
import random
import sklearn.model_selection as ms
import tensorflow as tf
import time

HEIGHT = 224
WIDTH = 224
CHANNELS = 3
BATCH_SIZE = 5
EPOCHS = 5

CHECKPOINT_PATH = os.path.join("checkpoint","cp.ckpt")
LOG_PATH = os.path.join("log","fit",datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

def _get_img(filename, label):
    img = tf.io.read_file(filename)
    img = tf.image.decode_jpeg(img, channels=CHANNELS)
    img = (tf.cast(img, tf.float32)/127.5) - 1
    img = tf.image.resize(img, (HEIGHT, WIDTH))
    return img, label

def get_data(folder):
    labelss = [x for x in os.listdir(folder) if x[0] != '.']
    print(labelss)
    with open('labels.txt', 'w') as f:
        for l in labelss:
            f.write(l+'\n')
    filenames = []
    labels = []
    index = 0
    for label in labelss:
        files = [os.path.join(folder,label,f) for f in os.listdir(os.path.join(folder,label)) if f[0] != '.']
        random.shuffle(files)
        lab = [index for x in range(len(files))]
        index = index + 1
        filenames.extend(files)
        labels.extend(lab)
    print(filenames, labels)
    train_filenames, val_filenames, train_labels, val_labels = ms.train_test_split(
                            filenames, labels, train_size=0.8)
    train_data = tf.data.Dataset.from_tensor_slices(
        (tf.constant(train_filenames), tf.constant(train_labels)))
    val_data = tf.data.Dataset.from_tensor_slices(
        (tf.constant(val_filenames), tf.constant(val_labels)))
    train_data = (train_data.map(_get_img).shuffle(buffer_size=1000).batch(BATCH_SIZE))
    val_data = (val_data.map(_get_img).shuffle(buffer_size=1000).batch(BATCH_SIZE))
    return train_data, val_data

def train_model(model, folder):
    print("Getting data")
    train_data, val_data = get_data(folder)
    print(train_data)

    print("Training model")
    #model.load_weights(CHECKPOINT_PATH)
    checkpoint = tf.keras.callbacks.ModelCheckpoint(CHECKPOINT_PATH,
                                                monitor='val_loss',
                                                verbose=0,
                                                save_best_only=False,
                                                save_weights_only=False,
                                                mode='auto', save_freq=500)
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=LOG_PATH, histogram_freq=1, write_graph=True, write_images=True)
    model.fit(x=train_data,
            epochs=EPOCHS,
            verbose=1,
            validation_data=val_data,
            callbacks=[checkpoint, tensorboard_callback])
    tensorboard_callback.set_model(model)
    model.save(os.path.join("model", "1"))

def convert_tflite(model, folder):
    print("Converting model")
    converter = tf.lite.TFLiteConverter.from_saved_model("model/1/")
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()
    open("converted_model_quantized.tflite", "wb").write(tflite_model)

model = thebox.TheBox()
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])
model.build(input_shape=(None, HEIGHT, WIDTH, CHANNELS))
# To train:
train_model(model, 'dataset')
# To convert:
convert_tflite(model, 'dataset')