# Import all backend configs and nodes
from .backends.numpy import numpy_config
from .backends.numpy.NodesNumpy import *

from .backends.pytorch import pytorch_config
from .backends.pytorch.NodesPytorch import *

from .backends.tensorflow import tensorflow_config
from .backends.tensorflow.NodesTensorflow import *

from .backends.jax import jax_config
from .backends.jax.NodesJax import *

class BackendConfig:
    backend = 'numpy'

    def _load_backend_config():
        # Determine the backend config module dynamically based on self.backend
        if BackendConfig.backend == 'numpy':
            backend_module = numpy_config
        elif BackendConfig.backend == 'torch':
            backend_module = pytorch_config
        elif BackendConfig.backend == 'tensorflow':
            backend_module = tensorflow_config
        elif BackendConfig.backend == 'jax':
            backend_module = jax_config
        else:
            raise ValueError(f"Unsupported backend '{BackendConfig.backend}'")

        # Assign the appropriate attributes based on the loaded module
        BackendConfig.backend_classes = getattr(backend_module, 'backend_classes', {})
        BackendConfig.backend_variable_classes = getattr(backend_module, 'backend_variable_classes', {})
        BackendConfig.backend_valuation_and_grad_classes = getattr(backend_module, 'backend_valuation_and_grad_classes', {})
        BackendConfig.backend_result_classes = getattr(backend_module, 'backend_result_classes', {})

        # True / False. Bool that states if the backend is able to do differentiation of the recorded graph (e.g. false for Jax since it needs an executable)
        backend_graph_differentiation_bool = True # Default value
        BackendConfig.backend_graph_differentiation_bool = getattr(backend_module, 'backend_graph_differentiation_bool', backend_graph_differentiation_bool)

        # Set the backend_function_mappings attribute.
        backend_function_mappings  = None
        BackendConfig.backend_function_mappings = getattr(backend_module, 'backend_function_mappings', backend_function_mappings)


