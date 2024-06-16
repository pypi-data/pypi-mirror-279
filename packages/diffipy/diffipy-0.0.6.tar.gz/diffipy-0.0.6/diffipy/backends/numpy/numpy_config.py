from .NodesNumpy import *

backend_classes = {
    "numpy": {
        "exp": ExpNodeNumpy,
        "pow": PowNodeNumpy,
        "log": LogNodeNumpy,
        "sqrt": SqrtNodeNumpy,
        "cdf": CdfNodeNumpy,
        "erf": ErfNodeNumpy,
        "erfinv": ErfinvNodeNumpy,
        "max": MaxNodeNumpy,
        "sumVectorized": SumNodeVectorizedNumpy,
        "seed": lambda value: np.random.seed(seed=value),
        "if": IfNodeNumpy,
        "sin": SinNodeNumpy,
        "cos": CosNodeNumpy
    }
}

backend_variable_classes = {
    "numpy": {
        "randomVariable": RandomVariableNodeNumpy,
        "constant": ConstantNode,
        "input": VariableNode,
        "randomVariableNormal": RandomVariableNodeNumpyNormal
    }
}

backend_valuation_and_grad_classes = {
    "numpy": {
        "grad": DifferentiationNodeNumpy
    }
}

backend_result_classes = {
    "numpy": {
        "result": ResultNodeNumpy
    }
}

backend_graph_differentiation_bool = True

backend_function_mappings = {
        "constant" : "",
        "exp": "np.exp",
        "sin": "np.sin",
        "cos": "np.cos",
        "pow": "np.pow",
        "log": "np.log",
        "sqrt": "np.sqrt",
        "cdf": "np.cdf",
        "erf": "scipy.special.erf",
        "erfinv": "scipy.special.erfinv",
        "max": "np.max",
        "sumVectorized": "np.sum",
        "seed": "np.seed",
        "if": "np.where"
    }
