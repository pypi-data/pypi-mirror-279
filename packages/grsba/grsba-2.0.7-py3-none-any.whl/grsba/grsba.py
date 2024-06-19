import tensorflow as tf
import numpy as np

class GRSBA(tf.keras.Model):
    def __init__(self, num_inputs, num_outputs, t=2, c=1.0, kernel_initializer='he_normal', clip_value=1.0, units=60, activation='relu', optimizer='adam', learning_rate=0.001, loss='mse', patience=10, epochs=100, batch_size=32, verbose=1):
        super(GRSBA, self).__init__()
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.t = t
        self.c = c
        self.kernel_initializer = kernel_initializer
        self.clip_value = clip_value
        self.units = units
        self.activation = activation
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.loss = loss
        self.patience = patience
        self.epochs = epochs
        self.batch_size = batch_size
        self.verbose = verbose
        self.running = False

    def mod(self, value, modulus):
        """Applies modular arithmetic to wrap values around the modulus, creating a toroidal effect."""
        return tf.math.floormod(value, modulus)

    def call(self, inputs):
        a, s, r, w, v, u = tf.split(inputs, num_or_size_splits=self.num_inputs, axis=1)

        epsilon = 1e-10

        # Primeira parte da fórmula
        term1_numerator = v + (u - v) / (1 - (u * v) / (self.c ** 2) + epsilon)
        term1_denominator = 1 + (v * (u * v) / (1 - (u * v) / (self.c ** 2) + epsilon)) / (self.c ** 2)
        term1 = term1_numerator / (term1_denominator + epsilon)  # Evitar divisão por zero

        # Segunda parte da fórmula
        term2_numerator = 4 * w * r
        term2_denominator = np.pi * tf.sqrt(1 - (w * r) ** 2 / (self.c ** 2) + epsilon)
        term2 = term2_numerator / (term2_denominator + epsilon)  # Evitar divisão por zero

        # Aplicar o limite inverso de "a"
        term_limit = tf.pow(a + epsilon, -1)  # Adicionar epsilon para evitar divisão por zero

        result = (term1 + term2) * term_limit * self.t

        recursive_result = tf.concat([
            tf.expand_dims(self.mod(result[:, 0] + a, self.clip_value), axis=1),
            tf.expand_dims(self.mod(result[:, 1] + s, self.clip_value), axis=1),
            tf.expand_dims(self.mod(result[:, 2] + r, self.clip_value), axis=1),
            tf.expand_dims(self.mod(result[:, 3] + w, self.clip_value), axis=1),
            tf.expand_dims(self.mod(result[:, 4] + v, self.clip_value), axis=1),
            tf.expand_dims(self.mod(result[:, 5] + u, self.clip_value), axis=1)
        ], axis=1)

        combined_result = self.mod(result + recursive_result[:, 0], self.clip_value)

        x1 = combined_result + a
        y1 = self.mod(combined_result + s, self.clip_value)
        z1 = self.mod(combined_result + r, self.clip_value)
        x2 = self.mod(combined_result + w, self.clip_value)
        y2 = self.mod(combined_result + v, self.clip_value)
        z2 = self.mod(combined_result + u, self.clip_value)

        return tf.concat([x1, y1, z1, x2, y2, z2], axis=1)

    def custom_output_layer(self, x):
        return self.call(x)