from .NodesOperations import *

###
### Node that are used for differentiation, performance testing and graph analysis
###

##
## Differentiation node is created on the graph when .grad() is called for on a node
##
class DifferentiationNode(UnitaryNode):
    def __init__(self, operand, diffDirection):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]
        self.diffDirection = diffDirection
       
    def Run(self):
        return self.operand.Run()

    def __str__(self):
        return f"grad({str(self.operand)})"
    
##
## Result node is used within performance testing. It contains the logic to create optimized executables and eval/grad of these.
##
class ResultNode(Node):
    def __init__(self, operationNode):
        super().__init__()
        self.operationNode = operationNode

    def eval_and_grad_of_function(sef, myfunc, args_dict):
        raise NotImplementedError("Must be implemented in ResultNode of backend")
    
    def get_function_mappings(self):
        from .backend_config import BackendConfig
        BackendConfig = BackendConfig()
        return BackendConfig.backend_function_mappings

    def run_backend_specific_performance_tests(self, input_variables, diff_variables, warmup_iterations, test_iterations):
        
        ###
        ### 1. Check if graph differentiation is available and if so, run performance tests there
        ###

        if diff_variables is None: # If no directions are specified, use all input directions
            diff_variables = self.operationNode.get_inputs_with_diff()
            
        from .backend_config import BackendConfig
        BackendConfig = BackendConfig()
        BackendConfig.backend_graph_differentiation_bool
        run_graph_differentiation_performance_test = BackendConfig.backend_graph_differentiation_bool #BackendConfig.backend_graph_differentiation_bool[BackendConfig.backend]["differentiation_bool"]
        
        if run_graph_differentiation_performance_test:


            total_time = 0.0
            results_standard = []
            times = []

            for _ in range(warmup_iterations):
                result_standard = self.operationNode.eval()
                gradient_standard = self.operationNode.grad(diff_variables)

            for _ in range(test_iterations):
                tic = time.time()
                #z.value = pre_computed_random_variables
                result_standard = self.operationNode.eval()
                gradient_standard = self.operationNode.grad(diff_variables)

                toc = time.time()
                spent = toc - tic
                times.append(spent)
                total_time += spent
                results_standard.append(result_standard)

            # Compute runtimes for the runs
            mean_time_standard =  total_time / test_iterations
            variance_time_standard =  sum((time - mean_time_standard) ** 2 for time in times) / (test_iterations - 1)    

        ###
        ### 2. Test performance of optimized executable (done for every backend)
        ###

        input_dict = {var.identifier: var.value for var in input_variables}

        diff_dict = {var.identifier: var.value for var in diff_variables}
        variable_dict = {var.identifier for var in diff_variables}

        myfunc = self.operationNode.get_optimized_executable()

        time_total_optimized = 0
        times_optimized = []
        results_optimized = []

        for _ in range(warmup_iterations):
            result_optimized, gradient_optimized = self.eval_and_grad_of_function(myfunc, input_dict, diff_dict)

        for _ in range(test_iterations):
            tic = time.time()

            result_optimized, gradient_optimized = self.eval_and_grad_of_function(myfunc, input_dict, diff_dict)

            toc = time.time()
            spent = toc - tic
            times_optimized.append(spent)
            time_total_optimized += spent

            results_optimized.append(result_optimized)

        # Compute runtimes
        mean_time_optimized = time_total_optimized / test_iterations
        variance_time_optimized = sum((time - mean_time_optimized) ** 2 for time in times_optimized) / (test_iterations - 1)

        # Output results in table format
        if BackendConfig.backend == 'numpy': # Header only printed the first time (by default numpy)
            print("{:<20} {:<12} {:<15} {:<20}{:<16}{:<16}".format('Backend', 'Eval-Result', 'mean runtime', 'variance runtime', 'gradient directions: ', str(variable_dict)))
        if run_graph_differentiation_performance_test: # Graph differentiation result only printed if available
            print("{:<20} {:<12.6f} {:<15.6f} {:<20.6f}{:<16}".format(BackendConfig.backend, sum(results_standard) / test_iterations, mean_time_standard, variance_time_standard, str(gradient_standard)))
        print("{:<20} {:<12.6f} {:<15.6f} {:<20.6f}{:<16}".format(BackendConfig.backend+ "_as_func", sum(results_optimized) / test_iterations, mean_time_optimized, variance_time_optimized, str(gradient_optimized)))


        def reorder_inputs_with_diff(all_inputs, inputs_with_diff):
            order_dict = {obj: idx for idx, obj in enumerate(all_inputs)}
            common_inputs_with_diff = [obj for obj in inputs_with_diff if obj in order_dict]
            sorted_inputs_with_diff = sorted(common_inputs_with_diff, key=lambda x: order_dict[x])
            return sorted_inputs_with_diff
   