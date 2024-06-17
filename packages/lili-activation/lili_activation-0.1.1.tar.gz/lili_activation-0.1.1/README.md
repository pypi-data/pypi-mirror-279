# lili_activation_keras

## Description
`lili_activation` is a custom activation function designed for TensorFlow and Keras frameworks. This package introduces `fnm3`, a sine-based transformation activation function that provides an alternative to traditional activation functions like ReLU or sigmoid. The `fnm3` function is particularly useful in scenarios where traditional activation functions might not capture complex patterns effectively.

## Installation
Install `lili_activation` directly from PyPI using pip:

```bash
pip install lili_activation
```
Ensure that you have pip updated and tensorflow installed in your environment, as lili_activation_keras depends on TensorFlow.

## Usage
To use fnm3 in your Keras model, follow these steps:

import tensorflow as tf

from lili_activation import fnm3

## Simple model example using `fnm3` as the activation function
model = tf.keras.Sequentia([
    tf.keras.layers.Dense(10, input_shape=(10,), activation=fnm3),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy')
model.summary()

## Features
Non-monotonic: Introduces a controlled non-monotonic that may be more suitable in scenarios where the relationships among input data are complex.

Innovative: Explores new avenues in activation functions that could prove beneficial in certain types of neural networks.

## Contributions
Contributions are always welcome. If you have ideas for improvements or extensions, please feel free to create an issue or pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
Lili Chen - lilichen577@gmail.com

## Acknowledgements
Special thanks to the TensorFlow and Keras community for providing an excellent platform for the experimentation and development of new ideas in machine learning.
