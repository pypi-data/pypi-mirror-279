# Import the nodes from which the following classes will inherit
from ...Node import *
from ...NodesVariables import *
from ...NodesOperations import *
from ...NodesDifferentiation import *
from ..BackendHelper import *

# Import backend specific packages
import torch

###
### PyTorch specific nodes.
###

class VariableNodeTorch(VariableNode):
    def __init__(self, value, identifier=None):
        super().__init__(value, identifier)
        self.value = torch.tensor(self.value, requires_grad=True)
        self.require_grad = True
        #self.value = self.value

    def Run(self):
        return self.value

class RandomVariableNodeTorch(RandomVariableNode):
    def NewSample(self, sampleSize = 1):
        self.SampleSize = sampleSize
        z_torch = torch.normal(mean=0, std=1, size=(1,sampleSize))
        self.value = 0.5 * (1 + torch.erf(z_torch / torch.sqrt(torch.tensor(2.0))))

class RandomVariableNodeTorchNormal(RandomVariableNode):
    def NewSample(self, sampleSize = 1):
        self.SampleSize = sampleSize
        self.value = torch.normal(mean=0, std=1, size=(1,sampleSize))

class ConstantNodeTorch(ConstantNode):
    def Run(self):
        return torch.tensor(self.value)
    def __str__(self):
        return f"constant({str(self.value)})"

class SinNodeTorch(SinNode):
    def Run(self):
        return torch.sin(self.operand.Run())
    
class CosNodeTorch(CosNode):
    def Run(self):
        return torch.cos(self.operand.Run())

class ExpNodeTorch(ExpNode):
    def Run(self):
        return torch.exp(self.operand.Run())

class LogNodeTorch(LogNode):
    def Run(self):
        return torch.log(self.operand.Run())
    
class SqrtNodeTorch(SqrtNode):
    def Run(self):
        return torch.sqrt(self.operand.Run())

class PowNodeTorch(PowNode):
    def Run(self):
        return torch.pow(self.left.Run(), self.right.Run())

class CdfNodeTorch(CdfNode):
    def Run(self):
        return 0.5 * (torch.erf(self.operand.Run() / torch.sqrt(torch.tensor(2.0))) + 1.0 )

class ErfNodeTorch(ErfNode):
    def Run(self):
        return torch.erf(self.operand.Run())
    
class ErfinvNodeTorch(ErfinvNode):
    def Run(self):
        return torch.erfinv(self.operand.Run())
    
class MaxNodeTorch(MaxNode):
    def Run(self):
        return torch.maximum(self.left.Run(), self.right.Run())

class SumNodeVectorizedTorch(Node):
    def __init__(self, operands):
        super().__init__()
        self.operands = self.ensure_node(operands)
        self.parents = [self.operands]

    def __str__(self):
        return f"sumVectorized({str(self.operands)})"

    def Run(self):
        return torch.sum(self.operands.Run())
    
    def get_inputs(self):
        return self.operands.get_inputs()
    def get_inputs_with_diff(self):
        return self.operands.get_inputs_with_diff()
    def get_input_variables(self):
        return self.operands.get_input_variables()

class IfNodeTorch(IfNode):
    def __init__(self, condition, true_value, false_value):
      super().__init__(condition, true_value, false_value)

    def Run(self):
      condition_value = self.condition.Run()
      true_value = self.true_value.Run()
      false_value = self.false_value.Run()
      return torch.where(condition_value, true_value, false_value)
    
##
## Differentiation node is created on the graph when .grad() is called for on a node
##
class DifferentiationNodeTorch(DifferentiationNode):
    def __init__(self, operand, diffDirection):
        super().__init__(operand, diffDirection)

    def backend_specific_grad(self):
        # Handle the case where self.diffDirection is a list
        if isinstance(self.diffDirection, list):
            derivatives = []
            for direction in self.diffDirection:
                # Reset derivative graph for each tensor
                if direction.value.grad is not None:
                    direction.value.grad.zero_()
                forward_evaluation = self.Run()

                # Backward pass
                forward_evaluation.backward()

                # Get the gradient
                derivative = direction.value.grad.item()
                derivatives.append(derivative)
            return derivatives
        else:
            # Handle the case where self.diffDirection is a single object
            # Reset derivative graph
            if self.diffDirection.value.grad is not None:
                self.diffDirection.value.grad.zero_()
            forward_evaluation = self.Run()

            # Backward pass
            forward_evaluation.backward()

            # Get the gradient
            derivative = self.diffDirection.value.grad.item()
            return derivative
    
##
## Result node is used within performance testing. It contains the logic to create optimized executables and eval/grad of these.
##
class ResultNodeTorch(ResultNode):
    def __init__(self, operationNode):
        super().__init__(operationNode)

    def eval(self):
        return self.operationNode.Run().item()
        
    def eval_and_grad_of_function(sef, myfunc, input_dict, diff_dict):
        
        result = myfunc(**input_dict)

        for key in diff_dict: #Reset all gradients first
            diff_dict[key].grad = None

        result.backward()

        gradient = []
        for key in diff_dict:
            gradient_entry = diff_dict[key].grad
            gradient.append( gradient_entry)
        return result, gradient


    def create_optimized_executable(self):
            expression = str(self.operationNode)

            function_mappings = self.get_function_mappings()

            for key, value in function_mappings.items():
                expression = expression.replace(key, value)

            #expression = expression.replace('exp', 'torch.exp').replace('sqrt', 'torch.sqrt').replace('log', 'torch.log').replace('sin', 'torch.sin')
            input_names = self.operationNode.get_input_variables()

            torch_func = BackendHelper.create_function_from_expression(expression, input_names,  {'torch': torch})

            # Wrap it such that it can get values as inputs
            def myfunc_wrapper(func):
                def wrapped_func(*args):#, **kwargs):
                    # Convert all positional arguments to torch.tensor
                    converted_args = [torch.tensor(arg.value) for arg in args]
                    
                    # # Convert all keyword arguments to torch.tensor
                    # converted_kwargs = {key: torch.tensor(value) for key, value in kwargs.items()}
                    
                    # Call the original function with converted arguments
                    return func(*converted_args)#, **converted_kwargs)
                
                return wrapped_func

            return torch_func#myfunc_wrapper(torch_func) #returning it in such a way that it needs tensor inputs for now