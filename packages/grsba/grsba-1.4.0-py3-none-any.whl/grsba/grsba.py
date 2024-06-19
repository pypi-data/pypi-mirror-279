import time
import threading
import tensorflow as tf
import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, Lambda
from keras.callbacks import EarlyStopping
import keras.backend as K

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

        # Debugging: imprimir valores intermediários
        print("Inputs:", inputs)
        print("Term1 numerator:", term1_numerator)
        print("Term1 denominator:", term1_denominator)
        print("Term1:", term1)
        print("Term2 numerator:", term2_numerator)
        print("Term2 denominator:", term2_denominator)
        print("Term2:", term2)
        print("Term limit:", term_limit)
        print("Result:", result)

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
        def prediction_loop():
            while self.running:
                predictions = self.predict(input_data)
                update_callback(predictions)
                time.sleep(interval)

        self.running = True
        prediction_thread = threading.Thread(target=prediction_loop)
        prediction_thread.start()

    def stop_prediction(self):
        """Stop the continuous prediction loop."""
        self.running = False

    def get_parameters(self):
        """Returns the current parameters of the GRSBA model."""
        return self.parameters