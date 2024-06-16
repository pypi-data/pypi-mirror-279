from .Node import Node
from .NodesVariables import *
from .NodesOperations import *
from .backend_config import *

#
# Main methods that are used for graph generation:
# - Each method creates a new object of the Node class.
# - The methods use the class Config for looking up specifics (e.g. usage of np.exp(), torch.exp(), or tensor.exp(), etc.)
#

# Load initial backend config (numpy by default)
BackendConfig._load_backend_config()

def setBackend(backend):
    BackendConfig.backend = backend
    BackendConfig._load_backend_config()
    
def variable(value, var_type='input'):
    if var_type == 'randomVariable':
        random_variable_class = BackendConfig.backend_variable_classes[BackendConfig.backend]["randomVariable"]
        return random_variable_class(value)
    elif var_type == 'constant':
        constant_class = BackendConfig.backend_variable_classes[BackendConfig.backend]["constant"]
        return constant_class(value)
    else:
        variable_class = BackendConfig.backend_variable_classes[BackendConfig.backend]["input"]
        return variable_class(value)

def variable(value, var_type='input', var_name=None):
    if var_type == 'randomVariable':
        random_variable_class = BackendConfig.backend_variable_classes[BackendConfig.backend]["randomVariable"]
        return random_variable_class(value, var_name)
    elif var_type == 'constant':
        constant_class = BackendConfig.backend_variable_classes[BackendConfig.backend]["constant"]
        return constant_class(value)
    elif var_type == 'randomVariableNormal':
        random_variable_class = BackendConfig.backend_variable_classes[BackendConfig.backend]["randomVariableNormal"]
        return random_variable_class(value, var_name)
    else:
        variable_class = BackendConfig.backend_variable_classes[BackendConfig.backend]["input"]
        return variable_class(value, var_name)

def constant(value):
    return ConstantNode(value)

def sin(operand):
    sin_class = BackendConfig.backend_classes[BackendConfig.backend]["sin"]
    return sin_class(operand)

def cos(operand):
    sin_class = BackendConfig.backend_classes[BackendConfig.backend]["cos"]
    return sin_class(operand)

def exp(operand):
    exp_class = BackendConfig.backend_classes[BackendConfig.backend]["exp"]
    return exp_class(operand)

def add(left, right):
    return AddNode(left, right)

def sub(left, right):
    return SubNode(left, right)

def mul(left, right):
    return MulNode(left, right)

def div(left, right):
    return DivNode(left, right)

def neg(operand):
    return NegNode(operand)

def log(operand):
    log_class = BackendConfig.backend_classes[BackendConfig.backend]["log"]
    return log_class(operand)

def sqrt(operand):
    sqrt_class = BackendConfig.backend_classes[BackendConfig.backend]["sqrt"]
    return sqrt_class(operand)

def cdf(operand):
    cdf_class = BackendConfig.backend_classes[BackendConfig.backend]["cdf"]
    return cdf_class(operand)

def erf(operand):
    erf_class = BackendConfig.backend_classes[BackendConfig.backend]["erf"]
    return erf_class(operand)

def erfinv(operand):
    erfinv_class = BackendConfig.backend_classes[BackendConfig.backend]["erfinv"]
    return erfinv_class(operand)

def max(left, right):
    max_class = BackendConfig.backend_classes[BackendConfig.backend]["max"]
    return max_class(left, right)

def zeros(N):
    return [ConstantNode(0) for _ in range(N)]

def sum(operands):
    if isinstance(operands, Node):
        sum_class = BackendConfig.backend_classes[BackendConfig.backend]["sumVectorized"]
    else:
        sum_class = SumNode
    return sum_class(operands)

def seed(value):
    seed_class = BackendConfig.backend_classes[BackendConfig.backend]["seed"]
    return seed_class(value)

def if_(condition, true_value, false_value):
    if_class = BackendConfig.backend_classes[BackendConfig.backend]["if"]
    return if_class(condition, true_value, false_value)



