from .NodesTensorflow import *

backend_classes = {
    "tensorflow": {
        "exp": ExpNodeTF,
        "pow": PowNodeTF,
        "log": LogNodeTF,
        "sqrt": SqrtNodeTF,
        "cdf": CdfNodeTF,
        "erf": ErfNodeTF,
        "erfinv": ErfinvNodeTF,
        "max": MaxNodeTF,
        "sumVectorized": SumNodeVectorizedTF,
        "seed": lambda value: tf.random.set_seed(value),
        "if": IfNodeTF,
        "sin": SinNodeTF,
        "cos": CosNodeTF
    }
}

backend_variable_classes = {
    "tensorflow": {
        "randomVariable": RandomVariableNodeTF,
        "constant": ConstantNodeTF,
        "input": VariableNodeTF,
        "randomVariableNormal": RandomVariableNodeTFNormal
    }
}

backend_valuation_and_grad_classes = {
    "tensorflow": {
        "grad": DifferentiationNodeTF
    }
}

backend_result_classes = {
    "tensorflow": {
        "result": ResultNodeTF
    }
}


backend_graph_differentiation_bool = True

backend_function_mappings = {
        #"constant" : "tf.Variable",
        "exp": "tf.exp",
        "sin": "tf.sin",
        "cos": "tf.cos",
        "pow": "tf.pow",
        "log": "tf.log",
        "sqrt": "tf.sqrt",
        "cdf": "tf.cdf",
        "erf": "tf.erf",
        "erfinv": "tf.erfinv",
        "max": "tf.max",
        "sumVectorized": "tf.math.reduce_sum",
        "seed": "tf.seed",
        "if": "tf.where"
    }
