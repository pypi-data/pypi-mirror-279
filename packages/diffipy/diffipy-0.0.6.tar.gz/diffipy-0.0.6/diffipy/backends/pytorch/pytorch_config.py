from .NodesPytorch import *

backend_classes = {
    "torch": {
        "exp": ExpNodeTorch,
        "pow": PowNodeTorch,
        "log": LogNodeTorch,
        "sqrt": SqrtNodeTorch,
        "cdf": CdfNodeTorch,
        "erf": ErfNodeTorch,
        "erfinv": ErfinvNodeTorch,
        "max": MaxNodeTorch,
        "sumVectorized": SumNodeVectorizedTorch,
        "seed": lambda value: torch.manual_seed(value),
        "if": IfNodeTorch,
        "sin": SinNodeTorch,
        "cos": CosNodeTorch
    }
}

backend_variable_classes = {
    "torch": {
        "randomVariable": RandomVariableNodeTorch,
        "constant": ConstantNodeTorch,
        "input": VariableNodeTorch,
        "randomVariableNormal": RandomVariableNodeTorchNormal
    }
}

backend_valuation_and_grad_classes = {
    "torch": {
        "grad": DifferentiationNodeTorch
    }
}

backend_result_classes = {
    "torch": {
        "result": ResultNodeTorch
    }
}

backend_graph_differentiation_bool = True

backend_function_mappings = {
            "constant" : "torch.tensor",
            "exp": "torch.exp",
            "sin": "torch.sin",
            "cos": "torch.cos",
            "pow": "torch.pow",
            "log": "torch.log",
            "sqrt": "torch.sqrt",
            "cdf": "torch.cdf",
            "erf": "torch.erf",
            "erfinv": "torch.erfinv",
            "max": "torch.max",
            "sumVectorized": "torch.sum",
            "seed": "torch.seed",
            "if": "torch.where"
    }
    