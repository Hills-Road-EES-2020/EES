import tensorflow as tf
import tensorflow.keras.layers as layers

class TheBox(tf.keras.Model):
    def __init__(self):
        super(TheBox, self).__init__()
        self.down1 = layers.Conv2D(8, kernel_size=3, activation='relu', name="Conv1")
        self.pool1 = layers.MaxPooling2D(pool_size=(2, 2), name="Pooling1")
        self.down2 = layers.Conv2D(24, kernel_size=3, activation='relu', name="Conv2")
        self.pool2 = layers.MaxPooling2D(pool_size=(2, 2), name="Pooling2")
        self.down3 = layers.Conv2D(64, kernel_size=3, activation='relu', name="Conv3")
        self.pool3 = layers.MaxPooling2D(pool_size=(2, 2), name="Pooling3")
        self.flatten = layers.Flatten()
        self.dense1 = layers.Dense(64, activation='relu', name="Dense1")
        self.dense2 = layers.Dense(14, activation='sigmoid', name="Dense2")
    
    def call(self, x):
        x = self.down1(x)
        x = self.pool1(x)
        x = self.down2(x)
        x = self.pool2(x)
        x = self.down3(x)
        x = self.pool3(x)
        x = self.flatten(x)
        x = self.dense1(x)
        x = self.dense2(x)
        return x
