import time
import numpy as np
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, Dense, Lambda
from keras.callbacks import EarlyStopping
import keras.backend as K
import threading

class GRSBA:
    def __init__(self, y, num_features=6, max_depth=5, units=256, activation='tanh', epochs=100, batch_size=32, patience=10, optimizer='adam', loss='mean_squared_error', verbose=1, t=None, learning_rate=0.0001, kernel_initializer='he_normal', clip_value=1.0):
        self.max_depth = max_depth
        self.units = units
        self.activation = activation
        self.epochs = epochs
        self.batch_size = batch_size
        self.patience = patience
        self.optimizer = optimizer
        self.loss = loss
        self.verbose = verbose
        self.y_shape = y.shape[1]  # Utilize a forma de y para definir num_numbers
        self.num_features = num_features
        self.t = t if t is not None else (time.time() % 60) / 60  # Default to current time if t is not provided
        self.learning_rate = learning_rate  # Adicionado learning_rate
        self.kernel_initializer = kernel_initializer  # Adicionado kernel_initializer
        self.clip_value = clip_value  # Adicionado clip_value
        self.model = self.create_model()
        self.running = False
        self.parameters = np.random.rand(num_features)  # Exemplo de inicialização de parâmetros

    def mod(self, value, modulus):
        """Applies modular arithmetic to wrap values around the modulus, creating a toroidal effect."""
        return tf.math.floormod(value, modulus)

    def custom_output_layer(self, inputs, depth=0):
        if (depth >= self.max_depth):
            return tf.zeros_like(inputs[:, :self.y_shape])  # Change here to match the output size

        u, v, w, r, s, a = inputs[:, 0], inputs[:, 1], inputs[:, 2], inputs[:, 3], inputs[:, 4], inputs[:, 5]
        c = 1.0  # Assuming c is 1.0
        epsilon = 1e-9  # Small constant to prevent division by zero

        # First part of the formula
        term1_numerator = v + (u - v) / (1 - (u * v) / (c ** 2) + epsilon)
        term1_denominator = 1 + (v * (u * v) / (1 - (u * v) / (c ** 2) + epsilon)) / (c ** 2)
        term1 = term1_numerator / (term1_denominator + epsilon)  # Avoid division by zero

        # Second part of the formula
        term2_numerator = 4 * w * r
        term2_denominator = np.pi * tf.sqrt(1 - (w * r) ** 2 / (c ** 2) + epsilon)
        term2 = term2_numerator / (term2_denominator + epsilon)  # Avoid division by zero

        # Apply the inverse limit of "a"
        term_limit = tf.pow(a + epsilon, -1)  # Add epsilon to prevent division by zero

        result = tf.pow((term1 + term2) * term_limit, self.t)  # Use the generic t

        # Recursive call to further bifurcate the space
        new_inputs = tf.stack([u, v, w, r, s, a], axis=1)
        recursive_result = self.custom_output_layer(new_inputs, depth + 1)

        # Ensure the recursive result has the correct shape with modular adjustments
        recursive_result = tf.concat([
            tf.expand_dims(self.mod(recursive_result[:, 0] + a, 0.5), axis=1),
            tf.expand_dims(self.mod(recursive_result[:, 1] + s, 0.5), axis=1),
            tf.expand_dims(self.mod(recursive_result[:, 2] + r, 0.5), axis=1),
            tf.expand_dims(self.mod(recursive_result[:, 3] + w, 0.5), axis=1),
            tf.expand_dims(self.mod(recursive_result[:, 4] + v, 0.5), axis=1),
            tf.expand_dims(self.mod(recursive_result[:, 5] + u, 0.5), axis=1)
        ], axis=1)

        # Combine current result with recursive result
        combined_result = self.mod(result + recursive_result[:, 0], 0.5)

        # Assume the output coordinates (x1, y1, z1, x2, y2, z2) are based on the combined result
        x1 = combined_result + a
        y1 = self.mod(combined_result + s, 0.5)
        z1 = self.mod(combined_result + r, 0.5)
        x2 = self.mod(combined_result + w, 0.5)
        y2 = self.mod(combined_result + v, 0.5)
        z2 = self.mod(combined_result + u, 0.5)

        return tf.stack([x1, y1, z1, x2, y2, z2], axis=1)

    def create_model(self):
        input_layer = Input(shape=(self.num_features,))  # Six inputs: u, v, w, r, s, a
        hidden_layer = Dense(self.units, activation=self.activation, kernel_initializer=self.kernel_initializer, kernel_regularizer=tf.keras.regularizers.l2(0.01))(input_layer)
        hidden_layer = Dense(self.units, activation=self.activation, kernel_initializer=self.kernel_initializer, kernel_regularizer=tf.keras.regularizers.l2(0.01))(hidden_layer)
        hidden_layer = Dense(self.units, activation=self.activation, kernel_initializer=self.kernel_initializer, kernel_regularizer=tf.keras.regularizers.l2(0.01))(hidden_layer)
        output_layer = Lambda(lambda x: self.custom_output_layer(x), output_shape=(self.y_shape,))(hidden_layer)

        # Usar o learning_rate ao compilar o modelo
        if self.optimizer == 'adam':
            optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate, clipvalue=self.clip_value)
        elif self.optimizer == 'sgd':
            optimizer = tf.keras.optimizers.SGD(learning_rate=self.learning_rate, clipvalue=self.clip_value)
        else:
            optimizer = self.optimizer

        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(optimizer=optimizer, loss=self.loss)
        return model

    def train(self, X, y):
        early_stopping = EarlyStopping(monitor='loss', patience=self.patience, restore_best_weights=True)
        history = self.model.fit(X, y, epochs=self.epochs, batch_size=self.batch_size, verbose=self.verbose, callbacks=[early_stopping])
        return history
    
    def predict(self, input_data):
        predictions = self.model.predict(input_data)
        predicted_numbers = np.argsort(predictions, axis=1)[:, -self.y_shape:]  # Seleciona os 'num_numbers' números com maior probabilidade
        return predicted_numbers

    def predict_continuously(self, input_data, update_callback, interval=1):
        """Continuously predict using the model and update the UI using the callback function."""
        self.running = True

        def _predict_loop():
            while self.running:
                predictions = self.predict(input_data)
                update_callback(predictions)
                time.sleep(interval)

        threading.Thread(target=_predict_loop, daemon=True).start()

    def stop_predicting(self):
        """Stop the continuous prediction loop."""
        self.running = False
    
    def get_parameters(self):
        return self.parameters