########################################################################################################################
########################################################################################################################
# File for storing the function used for the definition of QAOA
########################################################################################################################
########################################################################################################################
import random
from abc import ABC, abstractmethod
import pickle as pkl

# Packages needed
import cirq
import dimod
import numpy as np
from itertools import product, chain
from typing import Any

from .vqa_utils import VariationalCircuit, CostFunction
from .solver_utils import *


from os.path import exists

########################################################################################################################
# QAOA classes
########################################################################################################################
class QAOACirquit(VariationalCircuit):
    """
    Vanilla QAOA variational circuit.
    """
    def __init__(
        self, 
        model: dimod.BinaryQuadraticModel,
        p: int = 1,
        hyperparameters: list = None,
        qubit_name_to_object: dict[any, cirq.NamedQubit]=None
    ):

        # Storing the model to solve
        self.model = model

        # Storing the original spin model to implement the circuit
        if model.vartype == dimod.SPIN:
            self._model = model
        else:
            self._model = dimod.BinaryQuadraticModel(*model.to_ising(), dimod.SPIN)

        # Storing the number of layers
        self.p = p

        super().__init__(
            hyperparameters=hyperparameters, 
            qubit_name_to_object={var: cirq.NamedQubit(str(var)) for var in model.variables} if qubit_name_to_object==None 
                else qubit_name_to_object
        )


    def get_circuit_from_hyperparameters(self, hyperparameters: np.ndarray= None) -> cirq.Circuit:
        """
        Updates and returns the attribute `circuit` by generating a new `cirq.Circuit` object from the attribute `hyperparameters` or the input given.
        """

        if (type(hyperparameters) == np.ndarray and (hyperparameters != None).all()):
            self.hyperparameters = hyperparameters
        elif hyperparameters == None:
            pass
        else:
            raise ValueError(f"The hyperparameters must be an array of length {2*self.p}.")

        qasm =  get_qaoa_circuit(
            self.qubit_name_to_object, 
            self._model.linear, 
            self._model.quadratic, 
            self.hyperparameters[:self.p], 
            self.hyperparameters[self.p:]
        )

        self.qasm = qasm

        return qasm


    def sample(self, num_samples: int=100, hyperparameters: np.ndarray=None, original_basis=False, **kwargs):
        """
        Collects the samples from the stored vanilla QAOA circuit.

            args:
                num_samples: number of samples collected,
                hyperparameters: array of hyperparameters to evaluate (optional),
                original_basis: it returns the samples in the original basis if true else it returns the collected samples in the spin basis.

                **kwargs: optional arguments for the function qaoa_sampler

            returns: a list of solutions sampled from the QAOA circuit.
        """

        samples = qaoa_sampler(
            psi=self.qubit_name_to_object,
            model=self._model, 
            theta=hyperparameters if type(hyperparameters) == np.ndarray and (hyperparameters != None).all() 
                else self.hyperparameters,
            p=self.p,
            num_samples=num_samples,
            **kwargs
        )

        return self._samples_to_observable_basis(samples) if original_basis else samples


    def _samples_to_observable_basis(self, samples: list[dict]):
        """
        Maps samples collected from QAOA to the original basis eigenvalues.
        """
        if self.model.vartype == dimod.BINARY:
            return [
                {var: 1 if meas==+1 else 0 for var, meas in sample.items()} for sample in samples
            ]
        else:
            return samples


class pQAOACircuit(VariationalCircuit):
    def __init__(
        self, 
        hyperparameters: np.ndarray, 
        model: dimod.BinaryQuadraticModel,
        models: list[dimod.BinaryQuadraticModel],
        p: int = 1,
        qubit_name_to_object: dict[any, cirq.NamedQubit] = None
    ):

        # Storing the model to solve
        self.model = model

        # Storing the original spin model to implement the circuit
        if model.vartype == dimod.SPIN:
            self._model = model
        else:
            self._model = dimod.BinaryQuadraticModel(*model.to_ising(), dimod.SPIN)

        # Storing the number of layers to use
        self.p = p

        self.qubit_name_to_object = {var: cirq.NamedQubit(str(var)) for var in model.variables} if qubit_name_to_object==None else qubit_name_to_object

       # Creating the qaoa slice circuit of the slices that must be glued up by the optimizer
        self.qaoa_slices = [
            QAOACirquit(
                model=slice_model,
                p=p,
                hyperparameters=hyperparameters[index],
                qubit_name_to_object={var: qb for var, qb in self.qubit_name_to_object.items() if var in slice_model.variables}
            ) for index, slice_model in enumerate(models)
        ]

        # We store a boolean to identify whether the parameters are in the slice or the optimizer format
        self._optimizer_format = False

        super().__init__(
            hyperparameters=hyperparameters, 
            qubit_name_to_object={
                var: cirq.NamedQubit(str(var)) for var in model.variables
            } if qubit_name_to_object==None else qubit_name_to_object
        )


    def get_circuit_from_hyperparameters(self, hyperparameters: np.ndarray=None) -> cirq.Circuit:
        """
        Updates the attribute `circuit` by generating a list of `cirq.Circuit` object of the slices from the attribute `hyperparameters` or the input given.
        """
        if type(hyperparameters) == np.ndarray and np.array([type(row) == np.ndarray for row in hyperparameters]).all() and len(hyperparameters) == len(self.qaoa_slices):
            self.hyperparameters = hyperparameters
        elif hyperparameters == None:
            pass
        else:
            raise ValueError(f"The hyperparameters must be an array of {len(self.hyperparameters)} arrays of length {2*self.p*len(self.qaoa_slices)}.")

        slice_format_hyperparameters = self._format_slice(self.hyperparameters, self.p, len(self.qaoa_slices)) if self._optimizer_format else self.hyperparameters

        qasms =  [
                qaoa_slice.get_circuit_from_hyperparameters(hyperparameters=slice_format_hyperparameters[i]) for i, qaoa_slice in enumerate(self.qaoa_slices)
        ]

        self.qasm = qasms

        return qasms
        

    def sample(self, num_samples=100, hyperparameters=None, original_basis=False, **kwargs):
        """
        Collects the samples from the stored vanilla QAOA circuit.

            args:
                num_samples: number of samples collected,
                hyperparameters: array of hyperparameters to evaluate (optional),
                original_basis: it returns the samples in the original basis if true else it returns the collected samples in the spin basis.

                **kwargs: optional arguments for the function qaoa_sampler

            returns: a list of solutions sampled from the QAOA circuit.
        """

        if self._optimizer_format:
            input_hyperparameters = self._format_slice(
                hyperparameters=hyperparameters if type(hyperparameters)==np.ndarray and (hyperparameters!=None).all() 
                else self.hyperparameters,
                p=self.p,
                num_slices=len(self.qaoa_slices)
            )
        else:
            input_hyperparameters = hyperparameters if type(hyperparameters)==np.ndarray and (hyperparameters!=None).all() else self.hyperparameters

        list_of_samples = [
            qaoa_sampler(
                psi=qaoa_slice.qubit_name_to_object,
                model=qaoa_slice._model, 
                theta=input_hyperparameters[i],
                p=qaoa_slice.p,
                num_samples=num_samples,
                **kwargs
            ) for i, qaoa_slice in enumerate(self.qaoa_slices)
        ]

        samples = self._glue_slices(list_of_samples)

        return self._samples_to_observable_basis(samples) if original_basis else samples


    def _samples_to_observable_basis(self, samples: list[dict]):
        """
        Maps samples collected from pQAOA to the original basis eigenvalues.
        """
        if self.model.vartype == dimod.BINARY:
            return [
                {var: 1 if meas==+1 else 0 for var, meas in sample.items()} for sample in samples
            ]
        else:
            return samples


    def _hyperparameters_optimizer_format(self):
        """
        transforms the hyperparameters to a vector containing them. This is needed for the optimizer
        """

        if (
                np.array([type(row) == np.ndarray for row in self.hyperparameters]).all() and 
                len(self.hyperparameters) == len(self.qaoa_slices)
        ):

            self.hyperparameters = np.array(list(chain.from_iterable(self.hyperparameters)))
            self._optimizer_format = True
        
        elif type(self.hyperparameters) == np.ndarray and (len(self.hyperparameters) == 2*self.p*len(self.qaoa_slices)):
            pass
        
        else:
            raise ValueError("Wrong hyperparameters format")


    def _hyperparameters_slice_format(self):
        """
        transorms the hyperparameters to a tensor containing the hyperparameters divided by slice
        """

        if (
            np.array([type(row) == np.ndarray for row in self.hyperparameters]).all() and 
            len(self.hyperparameters) == len(self.qaoa_slices)
        ):
            pass
        
        elif type(self.hyperparameters) == np.ndarray and (len(self.hyperparameters) == 2*self.p*len(self.qaoa_slices)):
            self.hyperparameters = self._format_slice(
                hyperparameters=self.hyperparameters, 
                p=self.p, 
                num_slices=len(self.qaoa_slices)
            )
            self._optimizer_format = False
        
        else:
            from debug import checkpoint
            checkpoint(type(self.hyperparameters), (len(self.hyperparameters) == 2*self.p*len(self.qaoa_slices)))
            raise ValueError("Wrong hyperparameters format")


    @staticmethod
    def _glue_slices(solutions: list[list[dict]]):

        full_sols = []
        for tuple_of_sols in product(*solutions):
            sol = dict()
            for slice_sol in tuple_of_sols:
                sol.update(slice_sol)
            full_sols.append(sol)

        return full_sols


    @staticmethod
    def _format_slice(hyperparameters: np.ndarray, p: int, num_slices: int):
        """
        Transforms a list of parameter in slice format
        
            args
                hyperparameters: vector of hyperparameters to divide
                p: layers of QAOA
                num_slices: the number of slices used in the pQAOA algorithm
            
            returns: hyperparameters object in the slice format
        """

        return np.array(
                [np.array(hyperparameters[i*2*p:(i+1)*2*p]) for i in range(num_slices)]
            )


class ppQAOACircuit(pQAOACircuit):
    """pQAOA but to optimize the parameter a elementwise operation is applied, instead of vectorial product"""
    def __init__(self, hyperparameters: np.ndarray, model: dimod.BinaryQuadraticModel, models: list[dimod.BinaryQuadraticModel], p: int = 1, qubit_name_to_object: dict[any, cirq.NamedQubit] = None):
        super().__init__(hyperparameters, model, models, p, qubit_name_to_object)


    @staticmethod
    def _glue_slices(solutions: list[list[dict]]):
        full_sols = []
        for tuple_of_sols in zip(*solutions):
            sol = dict()
            for slice_sol in tuple_of_sols:
                sol.update(slice_sol)
            full_sols.append(sol)

        return full_sols


class pQAOASingleParametersCircuit(pQAOACircuit):
    """
    Parallelized version of QAOA circuit with 2 parameters per layers
    """
    def __init__(
        self, 
        hyperparameters: np.ndarray, 
        model: dimod.BinaryQuadraticModel,
        models: list[dimod.BinaryQuadraticModel],
        p: int = 1,
        qubit_name_to_object: dict[any, cirq.NamedQubit] = None
    ):

        # Storing the model to solve
        self.model = model

        # Storing the original spin model to implement the circuit
        if model.vartype == dimod.SPIN:
            self._model = model
        else:
            self._model = dimod.BinaryQuadraticModel(*model.to_ising(), dimod.SPIN)

        # Storing the number of layers to use
        self.p = p

        self.qubit_name_to_object = {var: cirq.NamedQubit(str(var)) for var in model.variables} if qubit_name_to_object==None else qubit_name_to_object

       # Creating the qaoa slice circuit of the slices that must be glued up by the optimizer
        self.qaoa_slices = [
            QAOACirquit(
                model=slice_model,
                p=p,
                hyperparameters=hyperparameters,
                qubit_name_to_object={var: qb for var, qb in self.qubit_name_to_object.items() if var in slice_model.variables}
            ) for slice_model in models
        ]

        # We store a boolean to identify whether the parameters are in the slice or the optimizer format
        self._optimizer_format = False

        # Storing the hyperparameters
        self.hyperparameters=hyperparameters
        
        # Initializing the mapping between qubit name and qubit
        self.qubit_name_to_object={
                var: cirq.NamedQubit(str(var)) for var in model.variables
            } if qubit_name_to_object==None else qubit_name_to_object

        # Implementing the circuit
        self.qasm = self.get_circuit_from_hyperparameters()


    def sample(self, num_samples=100, hyperparameters=None, original_basis=False, **kwargs):
        """
        Collects the samples from the stored vanilla QAOA circuit.

            args:
                num_samples: number of samples collected,
                hyperparameters: array of hyperparameters to evaluate (optional),
                original_basis: it returns the samples in the original basis if true else it returns the collected samples in the spin basis.

                **kwargs: optional arguments for the function qaoa_sampler

            returns: a list of solutions sampled from the QAOA circuit.
        """
        list_of_samples = [
            qaoa_sampler(
                psi=qaoa_slice.qubit_name_to_object,
                model=qaoa_slice._model, 
                theta=hyperparameters if type(hyperparameters)==np.ndarray and len(hyperparameters)==self.p*2 and (hyperparameters!=None).all() else self.hyperparameters,
                p=qaoa_slice.p,
                num_samples=num_samples,
                **kwargs
            ) for qaoa_slice in self.qaoa_slices
        ]

        samples = self._glue_slices(list_of_samples)

        return self._samples_to_observable_basis(samples) if original_basis else samples


    def _hyperparameters_optimizer_format(self):
        self._optimizer_format = True
        return self.hyperparameters


    def _hyperparameters_slice_format(self):
        self._optimizer_format = False
        return self.hyperparameters


    def get_circuit_from_hyperparameters(self, hyperparameters: np.ndarray=None) -> cirq.Circuit:
        """
        Updates the attribute `circuit` by generating a list of `cirq.Circuit` object of the slices from the attribute `hyperparameters` or the input given.
        """
        if type(hyperparameters) == np.ndarray and np.array([type(row) == np.ndarray for row in hyperparameters]).all() and len(hyperparameters) == len(self.qaoa_slices):
            self.hyperparameters = hyperparameters
        elif hyperparameters == None:
            pass
        else:
            raise ValueError(f"The hyperparameters must be an array of {len(self.hyperparameters)} arrays of length {2*self.p*len(self.qaoa_slices)}.")

        slice_format_hyperparameters = self._format_slice(self.hyperparameters, self.p, len(self.qaoa_slices)) if self._optimizer_format else self.hyperparameters

        qasms =  [
                qaoa_slice.get_circuit_from_hyperparameters(hyperparameters=slice_format_hyperparameters) for i, qaoa_slice in enumerate(self.qaoa_slices)
        ]

        self.qasm = qasms

        return qasms


    @staticmethod
    def _format_slice(hyperparameters: np.ndarray, p: int, num_slices: int):
        return hyperparameters


class ppQAOASingleParametersCircuit(pQAOASingleParametersCircuit):
    """pQAOA but to optimize the parameter a elementwise operation is applied, instead of vectorial product"""
    def __init__(self, hyperparameters: np.ndarray, model: dimod.BinaryQuadraticModel, models: list[dimod.BinaryQuadraticModel], p: int = 1, qubit_name_to_object: dict[any, cirq.NamedQubit] = None):
        super().__init__(hyperparameters, model, models, p, qubit_name_to_object)


    @staticmethod
    def _glue_slices(solutions: list[list[dict]]):
        full_sols = []
        for tuple_of_sols in zip(*solutions):
            sol = dict()
            for slice_sol in tuple_of_sols:
                sol.update(slice_sol)
            full_sols.append(sol)

        return full_sols


class SingleSliceQAOACircuit(QAOACirquit):
    def __init__(self, model: dimod.BinaryQuadraticModel, num_slices: int, slice_var_to_model_var: dict[Any: list[Any]], p: int = 1, hyperparameters: list = None, qubit_name_to_object: dict[any: cirq.NamedQubit] = None):        
        super().__init__(model, p, hyperparameters, qubit_name_to_object)

        # Storing the nimber of slices
        self.num_slices = num_slices

        # Store the mapping between the variables of the slice model to the variables of the model to evaluate
        self.slice_var_to_model_var = slice_var_to_model_var


    def sample(self, num_samples=100, hyperparameters=None, original_basis=False, **kwargs):
        """
        Collects the samples from the stored vanilla QAOA circuit.

            args:
                num_samples: number of samples collected,
                hyperparameters: array of hyperparameters to evaluate (optional),
                original_basis: it returns the samples in the original basis if true else it returns the collected samples in the spin basis.

                **kwargs: optional arguments for the function qaoa_sampler

            returns: a list of solutions sampled from the QAOA circuit.
        """

        slice_samples = qaoa_sampler(
                psi=self.qubit_name_to_object,
                model=self._model, 
                theta=hyperparameters if type(hyperparameters)==np.ndarray and (hyperparameters!=None).all() else self.hyperparameters,
                p=self.p,
                num_samples=num_samples,
                **kwargs
            )

        samples = self._glue_slices(
            self._slice_sol_to_model(slice_samples)
        )

        return self._samples_to_observable_basis(samples) if original_basis else samples


    @staticmethod
    def _glue_slices(solutions: list[list[dict]]):

        full_sols = []
        for tuple_of_sols in product(*solutions):
            sol = dict()
            for slice_sol in tuple_of_sols:
                sol.update(slice_sol)
            full_sols.append(sol)

        return full_sols
    

    def _slice_sol_to_model(self, samples: list[dict]):
        return [
            [
                {self.slice_var_to_model_var[var][index]: value for var, value in sol.items()} for sol in samples
            ] for index in range(self.num_slices)
        ]


class QAOACostFunction(CostFunction):
    """
    Cost function that represents the Hamiltonian to evaluate the output of a vanilla QAOA circuit.
    """
    def __init__(self, 
        objective_function: dimod.BinaryQuadraticModel
    ):
        super().__init__(objective_function)


    def evaluate_samples(self, solutions: list[dict]):
        """
        Returns the mean energy of the evaluated samples according to the implemented final Hamiltonian of a vanilla QAOA circuit.
        """

        average_magnetization_solution = {
            key: np.mean([sample[key] for sample in solutions]) for key in next(iter(solutions)).keys()
        }

        return np.mean(self.objective_function.energy(average_magnetization_solution))


########################################################################################################################
# Functions to generate the circuits
########################################################################################################################

# Function for implementing the interaction energy term
def append_zz_term(qc, psi, q1, q2, gamma, quad_term):

    '''
    qc: cirq.Circuit() where the gates are going to be append || type == cirq.Circuit()
    psi: register of qubits implemented in the quantum circuit || type == dict
    q1, q2: qubit indices || the type depends on the keys of psi
    gamma: QAOA parameter || type == float
    quad_term: quadratic terms of the Hamiltonian model || type == dict
    '''

    qc.append(cirq.CNOT(psi[q1], psi[q2]))
    qc.append(cirq.rz(gamma * quad_term[(q1, q2)])(psi[q2]))
    qc.append(cirq.CNOT(psi[q1],psi[q2]))


# Function for computing the local energy term
def append_z_term(qc, psi, q, gamma, lin_term):  # Preparing the gate decomposition for the linear term

    '''
    qc: cirq.Circuit() where the gates are going to be append || type == cirq.Circuit()
    psi: register of qubits implemented in the quantum circuit || type == dict
    q: qubit indicx || the type depends on the keys of psi
    gamma: QAOA parameter || type == float
    lin_term: linear terms of the Hamiltonian model || type == dict
    '''
    qc.append(cirq.rz(gamma * lin_term[q])(psi[q]))


# Obtaining the cost layer
def get_cost_operator_circuit(qc, psi, lin_term, quad_term, gamma):  # Computing the exponential matrix for H_f

    '''
    qc: cirq.Circuit() where the gates are going to be append || type == cirq.Circuit()
    psi: register of qubits implemented in the quantum circuit || type == dict
    lin_term: linear terms of the Hamiltonian model || type == dict
    quad_term: quadratic term of the Hamiltonian model || type == dict
    gamma: QAOA parameter || type == float
    '''

    for kl in lin_term.keys():
        append_z_term(qc, psi, kl, gamma, lin_term)

    for kq1, kq2 in quad_term.keys():
        append_zz_term(qc, psi, kq1, kq2, gamma, quad_term)


# Functions for implementing the mixing operator term
def append_x_term(qc, psi, q, beta):

    '''
    qc: cirq.Circuit() where the gates are going to be append || type == cirq.Circuit()
    psi: register of qubits implemented in the quantum circuit || type == dict
    q: qubit indicx || the type depends on the keys of psi
    beta: QAOA parameter || type == float
    '''

    qc.append(cirq.rx(beta)(psi[q]))


def get_mixer_operator_circuit(qc, psi, beta):

    '''
    qc: cirq.Circuit() where the gates are going to be append || type == cirq.Circuit()
    psi: register of qubits implemented in the quantum circuit || type == dict
    beta: QAOA parameter || type == float
    '''

    for var in psi.keys():
        append_x_term(qc, psi, var, beta)


def get_qaoa_circuit(psi, lin_term, quad_term, beta_list, gamma_list):

    '''
    psi: register of qubits implemented in the quantum circuit || type == dict
    lin_term: linear terms of the Hamiltonian model || type == dict
    quad_term: quadratic term of the Hamiltonian model || type == dict
    beta_list: list of QAOA parameters || type == list
    gamma_list: list of QAOA parameters || type == list
    '''
    assert (len(beta_list) == len(gamma_list))
    p = len(beta_list)  # infering number of QAOA steps from the parameters passed
    qc = cirq.Circuit()

    # first, apply a layer of Hadamards
    for qubit in psi.values():
        qc.append(cirq.H(qubit))

    # second, apply p alternating operators
    for i in range(p):
        get_cost_operator_circuit(qc, psi, lin_term, quad_term, gamma_list[i])
        get_mixer_operator_circuit(qc, psi, beta_list[i])

    return qc


########################################################################################################################
# Functions and classes for the classical optimization
########################################################################################################################

def qaoa_sampler(
    psi: dict[any, cirq.NamedQubit], 
    model: dimod.BinaryQuadraticModel, 
    theta: np.ndarray, 
    p: int, 
    num_samples: int, 
    num_subsamples: int=None, 
    solver: Solver=cirqSolver(),
    **kwargs
):
    '''
    collects the samples of the QAOA circuit from the provided backend.

        args:
            psi: register of qubits implemented in the quantum circuit,
            model: model of the combinatorial optimization problem,
            theta: vector of hyperparameters,
            p: number of QAOA layers,
            num_samples: number of samples to collect from the hardware,
            num_subsamples: number of solutions to consider from the samples collected.

            **kwargs: optional arguments of the method Solver.run
             
        returns: solutions in the spin basis
    '''

    if not num_subsamples:
        num_subsamples = num_samples

    qc = get_qaoa_circuit(psi, model.linear, model.quadratic, theta[:p], theta[p:])

    var_to_qubit_name = {var: qb.name for var, qb in psi.items()}
    qubit_name_to_var = {name: var for var, name in var_to_qubit_name.items()}

    for var, qb in psi.items():
        qc.append(cirq.measure(qb, key=var_to_qubit_name[var]))

    sols = solver.run(quantum_circuit=qc, num_samples=num_samples, **kwargs)

    if num_subsamples < num_samples:
        sampled_solutions = random.choices(sols, k=int(np.ceil(num_subsamples)))
    else:
        sampled_solutions = sols

    full_sols = [
        {qubit_name_to_var[var]: value for var, value in sample.items()}
        for sample in sampled_solutions
    ]

    return full_sols
