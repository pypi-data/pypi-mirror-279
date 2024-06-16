#
# Main class: Each operation '+,-,*,/,if,sum,...' and every variable 'constant,random,input,...' is represented by an object of the class node.
#

import time

class Node:
    
    #
    # Constructor, evaluation through the graph (Run()) and string representation of the nodes
    #

    def __init__(self):
        self.parents = []
    
    def Run(self):
        raise NotImplementedError("Must be implemented in subclasses")

    def __str__(self):
        raise NotImplementedError("Must be implemented in subclasses")

    ## Operator overloading to e.g. allow my.exp(x) + 3
    def __add__(self, other):
        from .NodesOperations import AddNode
        return AddNode(self, other)

    def __radd__(self, other):
        from .NodesOperations import AddNode
        return AddNode(other, self)

    def __sub__(self, other):
        from .NodesOperations import SubNode
        return SubNode(self, other)

    def __rsub__(self, other):
        from .NodesOperations import SubNode
        return SubNode(other, self)

    def __mul__(self, other):
        from .NodesOperations import MulNode
        return MulNode(self, other)

    def __rmul__(self, other):
        from .NodesOperations import MulNode
        return MulNode(other, self)

    def __truediv__(self, other):
        from .NodesOperations import DivNode
        return DivNode(self, other)

    def __rtruediv__(self, other):
        from .NodesOperations import DivNode
        return DivNode(other, self)

    def __neg__(self):
        from .NodesOperations import NegNode
        return NegNode(self)

    def __pow__(self, other):
        from .backend_config import BackendConfig
        pow_class = BackendConfig.backend_classes[BackendConfig.backend]["pow"]
        return pow_class(self, other)

    def __rpow__(self, other):
        from .backend_config import BackendConfig
        pow_class = BackendConfig.backend_classes[BackendConfig.backend]["pow"]
        return pow_class(self, other)

    def ensure_node(self, other):
        from .backend_config import BackendConfig
        if isinstance(other, Node):
            return other
        else:
            constant_class = BackendConfig.backend_variable_classes[BackendConfig.backend]["constant"]
            return constant_class(other)
    #
    # Comparison operators
    #
    def __gt__(self, other):
        from .NodesOperations import ComparisonNode
        return ComparisonNode(self, other, '>')

    def __lt__(self, other):
        from .NodesOperations import ComparisonNode
        return ComparisonNode(self, other, '<')

    def __ge__(self, other):
        from .NodesOperations import ComparisonNode
        return ComparisonNode(self, other, '>=')

    def __le__(self, other):
        from .NodesOperations import ComparisonNode
        return ComparisonNode(self, other, '<=')

    def __eq__(self, other):
        from .NodesOperations import ComparisonNode
        return ComparisonNode(self, other, '==')

    def __ne__(self, other):
        from .NodesOperations import ComparisonNode
        return ComparisonNode(self, other, '!=')
    
    #
    # Methods for differentiation
    #

    def grad(self, diffDirection = None):
        from .backend_config import BackendConfig
        grad_class = BackendConfig.backend_valuation_and_grad_classes[BackendConfig.backend]["grad"]
        if diffDirection is None:
            diffDirection = self.get_inputs_with_diff()
        instance_grad_class = grad_class(self, diffDirection)
        return instance_grad_class.backend_specific_grad()
    
    #
    # Additions for graph analysis
    #

    def get_inputs(self):
        raise NotImplementedError("Must be implemented in subclasses")
    
    def get_inputs_with_diff(self): # e.g. random samples won't be taken into account for grad
        raise NotImplementedError("Must be implemented in subclasses")
    
    def get_input_variables(self):
        raise NotImplementedError("Must be implemented in subclasses")
    
        
    def flatten_and_extract_unique_strings(self, arr):  # Ensure uniqueness
        unique_strings = set()
        def traverse(sub_arr):
            for item in sub_arr:
                if isinstance(item, str):
                    unique_strings.add(item)
                elif isinstance(item, list):
                    traverse(item)
        traverse(arr)
        return list(unique_strings)

    def flatten_list(self, nested_list):
        flat_list = []
        seen_ids = set()  # Set to keep track of seen identifiers
        
        def traverse(sub_list):
            for item in sub_list:
                if isinstance(item, list):
                    traverse(item)
                elif isinstance(item, Node):
                    if item.identifier not in seen_ids:
                        flat_list.append(item)
                        seen_ids.add(item.identifier)
                else:
                    flat_list.append(item)
            
        traverse(nested_list)
        return flat_list
    
    #
    # Additions for performance testing
    #

    def PerformanceIteration(self):
        a = self.Run()
        b = self.grad()
        return a + b

    def run_performance_test(self, input_variables, diff_variables, warmup_iterations=5, test_iterations=100):
        from .backend_config import BackendConfig
        BackendConfig = BackendConfig()
        eval_class = BackendConfig.backend_result_classes[BackendConfig.backend]["result"]
        instance_eval_class = eval_class(self)

        instance_eval_class.run_backend_specific_performance_tests(input_variables, diff_variables, warmup_iterations, test_iterations)
    
    def eval(self):
        from .backend_config import BackendConfig
        eval_class = BackendConfig.backend_result_classes[BackendConfig.backend]["result"]
        instance_eval_class = eval_class(self)
        return instance_eval_class.eval()#, instance_eval_class
    
    def create_result_class(self):
        from .backend_config import BackendConfig
        eval_class = BackendConfig.backend_result_classes[BackendConfig.backend]["result"]
        instance_eval_class = eval_class(self)
        return instance_eval_class
        
    #
    # Additions for exectuable function creations
    #

    def get_executable(self):
        # Create an executable that sets the input values and evaluates the graph
        from .NodesVariables import VariableNode

        inputs = self.get_inputs()
        def executable_func(*args):
            for input_node, arg in zip(inputs, args):
                input_node.set_value(arg)
            return self.Run()

        # Return a lambda function that calls executable_func
        return lambda *args: executable_func(*args)
    
    def get_optimized_executable(self):
        # Create an executable by code generation and that is hence independent of the graph 
        from .backend_config import BackendConfig
        eval_class = BackendConfig.backend_result_classes[BackendConfig.backend]["result"]
        instance_eval_class = eval_class(self)
        return instance_eval_class.create_optimized_executable()




#
# Unary (e.g. exp(x)) and binary nodes (x * y)
#

class UnitaryNode(Node):

    def get_inputs(self):
        return self.operand.get_inputs()
    def get_inputs_with_diff(self):
        return self.operand.get_inputs_with_diff()
    def get_input_variables(self):
        return self.operand.get_input_variables()

class BinaryNode(Node):

    def get_inputs(self):
        inputs = [self.left.get_inputs(), self.right.get_inputs()]
        return self.flatten_list([x for x in inputs if x])
    
    def get_inputs_with_diff(self):
        inputs = [self.left.get_inputs_with_diff(), self.right.get_inputs_with_diff()]
        return self.flatten_list([x for x in inputs if x])

    def get_input_variables(self):
        variableStrings = [self.left.get_input_variables(), self.right.get_input_variables()]
        return self.flatten_and_extract_unique_strings([x for x in variableStrings if x])




