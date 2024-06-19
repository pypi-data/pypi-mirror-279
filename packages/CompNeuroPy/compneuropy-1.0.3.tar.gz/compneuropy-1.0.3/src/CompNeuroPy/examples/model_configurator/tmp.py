import inspect


def trace_calls():
    # Get the call stack
    stack = inspect.stack()

    call_stack = []
    for frame in stack:
        # Get the function name
        function_name = frame.function
        # Check if it's a method of a class by looking for 'self' or 'cls'
        locals = frame.frame.f_locals
        if "self" in locals:
            class_name = locals["self"].__class__.__name__
            full_name = f"{class_name}.{function_name}"
        elif "cls" in locals:
            class_name = locals["cls"].__name__
            full_name = f"{class_name}.{function_name}"
        else:
            # If function_name is '<module>', replace it with the module name
            if function_name == "<module>":
                module_name = frame.frame.f_globals["__name__"]
                full_name = f"{module_name}"
            else:
                full_name = function_name
        call_stack.append(full_name)

    # Remove the first element of the call stack, which is the current function
    call_stack = call_stack[1:]

    # Get the name of the current function
    current_function_name = call_stack[0]

    # Reverse the call stack to get the order of the calls
    call_stack = call_stack[::-1]

    # Convert the call stack to a string
    call_stack = " -> ".join(call_stack)

    return current_function_name, call_stack


class MyClass:
    def method1(self):
        return self.method2()

    def method2(self):
        return self.method3()

    def method3(self):
        current_function_name, call_stack = trace_calls()
        print(f"Current function name: {current_function_name}")
        print(f"Call stack: {call_stack}")


# Create an instance of the class and call the first method
obj = MyClass()
obj.method1()
