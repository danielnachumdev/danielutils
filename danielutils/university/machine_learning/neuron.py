from .activation_functions import ActivationFunction


class Neuron:
    def __init__(self, activation: ActivationFunction, bias):
        self.activation = activation
        self.bias = bias

    def connect_after(self, successor: 'Neuron') -> None:
        pass

    def connect_before(self, predecessor: 'Neuron') -> None:
        pass


