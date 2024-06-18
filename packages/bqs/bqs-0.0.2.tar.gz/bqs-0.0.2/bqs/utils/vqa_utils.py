# General packages
from abc import ABC, abstractmethod
import numpy as np

# Packages for quantum computing
import dimod
import cirq



class VariationalCircuit(ABC):
    """
    Variational quantum circuit that store the information on how it is created and its hyperparameters.
    """
    def __init__(
        self,
        hyperparameters: np.ndarray,
        qubit_name_to_object: dict[any: cirq.NamedQubit] = None
    ):

        # Storing the hyperparameter
        self.hyperparameters = hyperparameters

        # Storing or getting the order of the qubits
        if qubit_name_to_object == None:
            self.qubit_name_to_object = {
                qubit.name: qubit for qubit in self.qasm.all_qubits()
            }
        else:
            self.qubit_name_to_object = qubit_name_to_object

        # Implementing the circuit
        self.qasm = self.get_circuit_from_hyperparameters()

    @abstractmethod
    def get_circuit_from_hyperparameters(self, hyperparameters: np.ndarray=None) -> cirq.Circuit:
        """
        Returns and stores a new circuit based on the attribute 'hyperparameters' .
        """
        pass

    @abstractmethod
    def sample(self, num_samples=100, hyperparameters=None):
        """
        Collectes samples from the circuit store in the attribute 'qasm' .
        """
        pass


class CostFunction(ABC):
    """
    Functions to evaluate to optimize the hyperparameters of a variational quantum circuit.
    """
    def __init__(
        self,
        objective_function: dimod.BinaryQuadraticModel,
    ):
        
        # The objective function to evaluate the states is stored
        self.objective_function = objective_function

    @abstractmethod
    def evaluate_samples(self, solutions):
        """
        Evaluates a list of solutions and it returns a float number that represent the energy of the evaluated cost function.

        The solutions must be stored as list of dictionary. whose keys are the name of the variable and values are the observed measurement.
        """
        pass
