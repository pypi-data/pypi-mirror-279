# Import the nodes from which the following classes will inherit
from ...Node import *
from ...NodesVariables import *
from ...NodesOperations import *
from ...NodesDifferentiation import *
from ..BackendHelper import *

# Import backend specific packages
import jax
import jax.numpy as jnp

###
### Jax specific nodes.
###

class VariableNodeJAX(VariableNode):
    def __init__(self, value, identifier=None):
        super().__init__(value, identifier)
        self.value = jnp.array(self.value)

    def Run(self):
        return self.value
    
class RandomVariableNodeJAX(RandomVariableNode):
    def NewSample(self, sampleSize=1):
        self.SampleSize = sampleSize
        z_jax = jax.random.normal(jax.random.PRNGKey(0), shape=(1, sampleSize))
        self.value = 0.5 * (1 + jax.scipy.special.erf(z_jax / jnp.sqrt(2.0)))

class RandomVariableNodeJAXNormal(RandomVariableNode):
    def NewSample(self, sampleSize=1):
        self.SampleSize = sampleSize
        self.value = jax.random.normal(jax.random.PRNGKey(0), shape=(1, sampleSize))

class ConstantNodeJAX(ConstantNode):
    def Run(self):
        return jnp.array(self.value)
    def __str__(self):
        return f"constant({str(self.value)})"

class ExpNodeJAX(ExpNode):
    def Run(self):
        return jnp.exp(self.operand.Run())
    
class SinNodeJAX(SinNode):
    def Run(self):
        return jnp.sin(self.operand.Run())
    
class CosNodeJAX(CosNode):
    def Run(self):
        return jnp.cos(self.operand.Run())

class LogNodeJAX(LogNode):
    def Run(self):
        return jnp.log(self.operand.Run())

class SqrtNodeJAX(SqrtNode):
    def Run(self):
        return jnp.sqrt(self.operand.Run())

class PowNodeJAX(PowNode):
    def Run(self):
        return jnp.power(self.left.Run(), self.right.Run())

class CdfNodeJAX(CdfNode):
    def Run(self):
        return 0.5 * (jax.scipy.special.erf(self.operand.Run() / jnp.sqrt(2.0)) + 1.0)

class ErfNodeJAX(ErfNode):
    def Run(self):
        return jax.scipy.special.erf(self.operand.Run())

class ErfinvNodeJAX(ErfinvNode):
    def Run(self):
        return jax.scipy.special.erfinv(self.operand.Run())

class MaxNodeJAX(MaxNode):
    def Run(self):
        return jnp.maximum(self.left.Run(), self.right.Run())

class SumNodeVectorizedJAX(Node):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]
    def __str__(self):
        return f"sumVectorized({str(self.operand)})"
    def Run(self):
        return jnp.sum(self.operand.Run())
    def get_inputs(self):
        return self.operand.get_inputs()
    def get_inputs_with_diff(self):
        return self.operand.get_inputs_with_diff()
    def get_input_variables(self):
        return self.operand.get_input_variables()

class IfNodeJAX(IfNode):
    def __init__(self, condition, true_value, false_value):
        super().__init__(condition, true_value, false_value)
    def Run(self):
        condition_value = self.condition.Run()
        true_value = self.true_value.Run()
        false_value = self.false_value.Run()
        return jnp.where(condition_value, true_value, false_value)

##
## Differentiation node is created on the graph when .grad() is called for on a node
##
class DifferentiationNodeJAX(DifferentiationNode):
    def __init__(self, operand, diffDirection):
        super().__init__(operand, diffDirection)
    def backend_specific_grad(self):

        input_variables = self.get_inputs()
        #print(input_variables)
        input_dict = {var.identifier: var.value for var in input_variables}

        myfunc = self.operand.get_optimized_executable()
        _, gradient = self.eval_and_grad_of_function(myfunc, input_dict, input_dict)

        if isinstance(self.diffDirection, list):
            gradients = {}
            for direction in self.diffDirection:
                if isinstance(direction, VariableNodeJAX):
                    gradient_key = direction.identifier
                else:
                    gradient_key = direction
                
                if gradient_key not in gradient:
                    raise ValueError(f"Gradient for '{gradient_key}' not found in the computed gradients.")
                
                gradients[gradient_key] = gradient[gradient_key]
            gradients_as_array = [value.block_until_ready().item() for value in gradients.values()]
            return gradients_as_array
        else:
            # Handle the case where diffDirection is not a list
            if isinstance(self.diffDirection, VariableNodeJAX):
                gradient_key = self.diffDirection.identifier
            else:
                gradient_key = self.diffDirection
            
            if gradient_key not in gradient:
                raise ValueError(f"Gradient for '{gradient_key}' not found in the computed gradients.")
           
            return gradient[gradient_key]
    
    def eval_and_grad_of_function(sef, myfunc, input_dict, diff_dict):
        result_optimized = myfunc(**input_dict)#s0=s0.value, K=K.value, r=r.value, sigma=sigma.value, dt = dt.value, z=pre_computed_random_variables)
        def myfunc_with_dict(args_dict):
            return myfunc(**args_dict)
        gradient_func = jax.grad(myfunc_with_dict)
        gradient_all_directions = gradient_func(input_dict)
        gradient = {key: gradient_all_directions[key] for key in diff_dict.keys()}
        return result_optimized, gradient
    
    def create_optimized_executable(self):
        expression = str(self.operationNode)
        function_mappings = self.get_function_mappings()
        for key, value in function_mappings.items():
            expression = expression.replace(key, value)
        input_names = self.operationNode.get_input_variables()
        numpy_func = BackendHelper.create_function_from_expression(expression, input_names,  {'jax': jax, 'jnp' : jax.numpy})
        #jitted_numpy_func = jit(nopython=True)(numpy_func)
        jax.make_jaxpr(numpy_func)
        return  numpy_func#jitted_numpy_func# numpy_func


##
## Result node is used within performance testing. It contains the logic to create optimized executables and eval/grad of these.
##
class ResultNodeJAX(ResultNode):
    def __init__(self, operationNode):
        super().__init__(operationNode)
    def eval(self):
        return self.operationNode.Run().item()
    
    def eval_and_grad_of_function(sef, myfunc, input_dict, diff_dict):
        result_optimized = myfunc(**input_dict)#s0=s0.value, K=K.value, r=r.value, sigma=sigma.value, dt = dt.value, z=pre_computed_random_variables)
        def myfunc_with_dict(args_dict):
            return myfunc(**args_dict)
        gradient_func = jax.grad(myfunc_with_dict)
        gradient_all_directions = gradient_func(input_dict)
        gradient = {key: gradient_all_directions[key] for key in diff_dict.keys()}
        return result_optimized, gradient
    
    def create_optimized_executable(self):
        expression = str(self.operationNode)
        function_mappings = self.get_function_mappings()
        for key, value in function_mappings.items():
            expression = expression.replace(key, value)
        input_names = self.operationNode.get_input_variables()
        numpy_func = BackendHelper.create_function_from_expression(expression, input_names,  {'jax': jax, 'jnp' : jax.numpy})
        #jitted_numpy_func = jit(nopython=True)(numpy_func)
        jax.make_jaxpr(numpy_func)
        return  numpy_func#jitted_numpy_func# numpy_func

