import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM

class Encoder(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, enc_units, batch_sz):
        super(Encoder, self).__init__()
        self.batch_sz = batch_sz
        self.enc_units = enc_units
        self.embedding = Embedding(vocab_size, embedding_dim)
        self.lstm = LSTM(self.enc_units, return_sequences=True, return_state=True, recurrent_initializer='glorot_uniform')

    def call(self, x, hidden):
        x = self.embedding(x)
        output, state = self.lstm(x, initial_state=hidden)
        return output, state

    def initialize_hidden_state(self):
        return [tf.zeros((self.batch_sz, self.enc_units))]
