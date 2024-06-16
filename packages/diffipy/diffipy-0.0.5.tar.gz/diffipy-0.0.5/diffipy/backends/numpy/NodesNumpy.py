# Import the nodes from which the following classes will inherit
from ...Node import *
from ...NodesVariables import *
from ...NodesOperations import *
from ...NodesDifferentiation import *
from ..BackendHelper import *

# Import backend specific packages
import numpy as np
import scipy.stats
import scipy.special
from numba import jit

###
### NumPy specific nodes.
###

class ExpNodeNumpy(ExpNode):
    def Run(self):
        return np.exp(self.operand.Run())
    
class SinNodeNumpy(SinNode):
    def Run(self):
        return np.sin(self.operand.Run())
    
class CosNodeNumpy(SinNode):
    def Run(self):
        return np.cos(self.operand.Run())
    
class LogNodeNumpy(LogNode):
    def Run(self):
        return np.log(self.operand.Run())
    
class SqrtNodeNumpy(SqrtNode):
    def Run(self):
        return np.sqrt(self.operand.Run())
    
class PowNodeNumpy(PowNode):
    def Run(self):
        return self.left.Run() ** self.right.Run()
    
class CdfNodeNumpy(CdfNode):
    def Run(self):
        return scipy.stats.norm.cdf(self.operand.Run())
    
class ErfNodeNumpy(ErfNode):
    def Run(self):
        return scipy.special.erf(self.operand.Run())

class ErfinvNodeNumpy(ErfinvNode):
    def Run(self):
        return scipy.special.erfinv(self.operand.Run())

class MaxNodeNumpy(MaxNode):
    def Run(self):
        return np.maximum(self.left.Run(), self.right.Run())

class RandomVariableNodeNumpy(RandomVariableNode):
    def NewSample(self, sampleSize = 1):
        self.value = np.random.uniform(size = sampleSize)

class RandomVariableNodeNumpyNormal(RandomVariableNode):
    def NewSample(self, sampleSize = 1):
        self.value = np.random.normal(size = sampleSize)

class SumNodeVectorizedNumpy(Node):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]
    def __str__(self):
        return f"sumVectorized({str(self.operand)})"
    def Run(self):
        return np.sum(self.operand.Run())
    def get_inputs(self):
        return self.operand.get_inputs()
    def get_inputs_with_diff(self):
        return self.operand.get_inputs_with_diff()
    def get_input_variables(self):
        return self.operand.get_input_variables()

class IfNodeNumpy(IfNode):
        def Run(self):
            condition_value = self.condition.Run()
            true_value = self.true_value.Run()
            false_value = self.false_value.Run()
            return np.where(condition_value, true_value, false_value)

##
## Differentiation node is created on the graph when .grad() is called for on a node
##
class DifferentiationNodeNumpy(DifferentiationNode):

    def __init__(self, operand, diffDirection):
        super().__init__(operand, diffDirection)

    def backend_specific_grad(self):
        result = self.Run()
        h = 0.00001
        # Handle the case where self.diffDirection is a list, hence Gradient
        if isinstance(self.diffDirection, list):
            gradients = []
            for direction in self.diffDirection:
                original_value = direction.value
                direction.value = original_value + h
                result_h = self.Run()
                gradient = (result_h - result) / h
                gradients.append(gradient)
                # Reset the value to its original state
                direction.value = original_value
            return gradients
        else:
            # Handle the case where self.diffDirection is a single diff direction
            original_value = self.diffDirection.value
            self.diffDirection.value = original_value + h
            result_h = self.Run()
            gradient = (result_h - result) / h
            # Reset the value to its original state
            self.diffDirection.value = original_value
            return gradient
    
##
## Result node is used within performance testing. It contains the logic to create optimized executables and eval/grad of these.
##
class ResultNodeNumpy(ResultNode):
    def __init__(self, operationNode):
        super().__init__(operationNode)
    def eval(self):
        return self.operationNode.Run()
       
    def eval_and_grad_of_function(self, func, input_dict, diff_dict, h=0.00001):
        result = func(**input_dict)
        gradients = {}
        for key in diff_dict:
            args_dict_shifted = input_dict.copy()
            args_dict_shifted[key] += h
            result_h = func(**args_dict_shifted)
            gradient = (result_h - result) / h
            gradients[key] = gradient
        
        return result, gradients
    
    def create_optimized_executable(self):
        expression = str(self.operationNode)
        
        function_mappings = self.get_function_mappings()

        for key, value in function_mappings.items():
            expression = expression.replace(key, value)

        input_names = self.operationNode.get_input_variables()

        numpy_func = BackendHelper.create_function_from_expression(expression, input_names,  {'np': np, 'scipy.special' : scipy.special})
        jitted_numpy_func = jit(nopython=True)(numpy_func)

        return  jitted_numpy_func# numpy_func
