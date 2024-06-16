
class BackendHelper:
    
    @staticmethod
    def create_function_from_expression(expression_string, expression_inputs, backend):
        # Generate the function definition as a string
        inputs = ", ".join(expression_inputs)
        function_code = f"def myfunc({inputs}):\n    return {expression_string}\n"

        # Compile the function code
        compiled_code = compile(function_code, "<string>", "exec")

        # Combine the provided backend with an empty dictionary to serve as the globals
        namespace = {**backend}
        exec(compiled_code, namespace)

        # Return the dynamically created function
        return namespace["myfunc"]
