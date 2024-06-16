from .NodesJax import *

backend_classes = {
    "jax": {
        "exp": ExpNodeJAX,
        "pow": PowNodeJAX,
        "log": LogNodeJAX,
        "sqrt": SqrtNodeJAX,
        "cdf": CdfNodeJAX,
        "erf": ErfNodeJAX,
        "erfinv": ErfinvNodeJAX,
        "max": MaxNodeJAX,
        "sumVectorized": SumNodeVectorizedJAX,
        "seed": lambda value: jax.random.PRNGKey(seed=value),
        "if": IfNodeJAX,
        "sin": SinNodeJAX,
        "cos": CosNodeJAX
    }
}

backend_variable_classes = {
    "jax": {
        "randomVariable": RandomVariableNodeJAX,
        "constant": ConstantNodeJAX,
        "input": VariableNodeJAX,
        "randomVariableNormal": RandomVariableNodeJAXNormal
    }
}

backend_valuation_and_grad_classes = {
    "jax": {
        "grad": DifferentiationNodeJAX
    }
}

backend_result_classes = {
    "jax": {
        "result": ResultNodeJAX
    }
}

backend_graph_differentiation_bool = False

backend_function_mappings = {
    "constant" : "",
    "exp": "jnp.exp",
    "sin": "jnp.sin",
    "cos": "jnp.cos",
    "pow": "jnp.pow",
    "log": "jnp.log",
    "sqrt": "jnp.sqrt",
    "cdf": "jnp.cdf",
    "erf": "jax.scipy.special.erf",
    "erfinv": "jax.scipy.special.erfinv",
    "max": "jnp.max",
    "sumVectorized": "jnp.sum",
    "seed": "jnp.seed",
    "if": "jnp.where"
}