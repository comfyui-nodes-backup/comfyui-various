import inspect
import math


NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}


def register_node(identifier: str, display_name: str):
    def decorator(cls):
        NODE_CLASS_MAPPINGS[identifier] = cls
        NODE_DISPLAY_NAME_MAPPINGS[identifier] = display_name

        return cls

    return decorator


def generate_functional_node(
    category: str,
    identifier: str,
    display_name: str,
    output_node: bool = False,
):
    def decorator(func):
        signature = inspect.signature(func)

        # generate INPUT_TYPES
        required_inputs = {}

        for name, param in signature.parameters.items():
            has_default = param.default is not param.empty
            param_type = param.annotation
            if param_type is int:
                if not has_default:
                    raise TypeError("INT input must have a default value")

                required_inputs[name] = (
                    "INT",
                    {
                        "default": param.default,
                        "min": -99999999999999999,
                        "max": 99999999999999999,
                    },
                )
            elif param_type is float:
                if not has_default:
                    raise TypeError("FLOAT input must have a default value")

                required_inputs[name] = (
                    "FLOAT",
                    {
                        "default": param.default,
                        "min": -99999999999999999.0,
                        "max": 99999999999999999.0,
                    },
                )
            elif param_type is str:
                if not has_default:
                    raise TypeError("STRING input must have a default value")

                required_inputs[name] = (
                    "STRING",
                    {"default": param.default, "multiline": False},
                )
            elif isinstance(param_type, str):
                if has_default:
                    raise TypeError("Custom input types cannot have default values")

                required_inputs[name] = (param_type,)
            else:
                raise NotImplementedError(
                    f"Unsupported functional node type: {param_type}"
                )

        # generate RETURN_TYPES
        if signature.return_annotation is signature.empty:
            raise TypeError("Functional node must have annotation for return type")
        elif not isinstance(signature.return_annotation, tuple):
            raise TypeError("Functional node must return a tuple")

        return_types = []
        for annot in signature.return_annotation:
            if isinstance(annot, str):
                return_types.append(annot)
            elif annot is int:
                return_types.append("INT")
            elif annot is float:
                return_types.append("FLOAT")
            elif annot is str:
                return_types.append("STRING")
            else:
                raise NotImplementedError(f"Unsupported return type: {annot}")

        @register_node(identifier, display_name)
        class FuncNode:
            CATEGORY = category

            INPUT_TYPES = lambda: {"required": required_inputs}

            RETURN_TYPES = tuple(return_types)

            OUTPUT_NODE = output_node

            FUNCTION = "execute"

            def execute(self, *args, **kwargs):
                return func(*args, **kwargs)

        print(f"identifier = {identifier}")
        print(f"display_name = {display_name}")
        print(f"INPUT_TYPES = {required_inputs}")
        print(f"RETURN_TYPES = {tuple(return_types)}")

        return func

    return decorator


@generate_functional_node("jamesWalker55", "JWInteger", "Integer")
def integer_value(value: int = 0) -> (int,):
    return (value,)


@generate_functional_node("jamesWalker55", "JWIntegerToFloat", "Integer to Float")
def integer_to_float(value: int = 0) -> (float,):
    return (float(value),)


@generate_functional_node("jamesWalker55", "JWIntegerAdd", "Integer Add")
def integer_sum(a: int = 0, b: int = 0) -> (int,):
    return (a + b,)


@generate_functional_node("jamesWalker55", "JWIntegerSub", "Integer Subtract")
def integer_sum(a: int = 0, b: int = 0) -> (int,):
    return (a - b,)


@generate_functional_node("jamesWalker55", "JWIntegerMul", "Integer Multiply")
def integer_sum(a: int = 0, b: int = 0) -> (int,):
    return (a * b,)


@generate_functional_node("jamesWalker55", "JWIntegerDiv", "Integer Divide")
def integer_sum(a: int = 0, b: int = 0) -> (float,):
    return (a / b,)


@generate_functional_node("jamesWalker55", "JWFloat", "Float")
def float_value(value: float = 0) -> (float,):
    return (value,)


@generate_functional_node("jamesWalker55", "JWFloatToInteger", "Float to Integer")
def float_to_integer(value: float = 0) -> (int,):
    return (round(value),)


@generate_functional_node("jamesWalker55", "JWFloatAdd", "Float Add")
def float_sum(a: float = 0, b: float = 0) -> (float,):
    return (a + b,)


@generate_functional_node("jamesWalker55", "JWFloatSub", "Float Subtract")
def float_sum(a: float = 0, b: float = 0) -> (float,):
    return (a - b,)


@generate_functional_node("jamesWalker55", "JWFloatMul", "Float Multiply")
def float_sum(a: float = 0, b: float = 0) -> (float,):
    return (a * b,)


@generate_functional_node("jamesWalker55", "JWFloatDiv", "Float Divide")
def float_sum(a: float = 0, b: float = 0) -> (float,):
    return (a / b,)
