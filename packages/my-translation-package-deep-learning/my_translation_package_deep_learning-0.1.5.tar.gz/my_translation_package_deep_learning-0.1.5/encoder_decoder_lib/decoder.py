import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM, Dense, Concatenate, Attention

class Decoder(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, dec_units, batch_sz):
        super(Decoder, self).__init__()
        self.batch_sz = batch_sz
        self.dec_units = dec_units
        self.embedding = Embedding(vocab_size, embedding_dim)
        self.lstm = LSTM(self.dec_units, return_sequences=True, return_state=True, recurrent_initializer='glorot_uniform')
        self.fc = Dense(vocab_size)
        self.attention = Attention()

    def call(self, x, hidden, enc_output):
        context_vector, attention_weights = self.attention([hidden, enc_output], return_attention_scores=True)
        context_vector = tf.reduce_sum(context_vector, axis=1)

        x = self.embedding(x)
        x = Concatenate(axis=-1)([tf.expand_dims(context_vector, 1), x])
        output, state = self.lstm(x)
        output = tf.reshape(output, (-1, output.shape[2]))
        x = self.fc(output)
        return x, state, attention_weights
