from typing import Dict
import ast


class _GetArgInfoHolder:
    @classmethod
    def extract_return_info(cls, source: str) -> Dict[str, str]:
        tree = ast.parse(source)
        func_def = tree.body[0]

        return_type = None
        if func_def.returns:
            return_type = ast.unparse(func_def.returns)
            if return_type.startswith("Tuple"):
                # Extract return variable names and their types
                return_expr = func_def.body[-1]
                if isinstance(return_expr, ast.Return):
                    if isinstance(return_expr.value, ast.Tuple):
                        elements = return_expr.value.elts
                        if isinstance(func_def.returns, ast.Subscript):
                            types = func_def.returns.slice
                            if isinstance(types, ast.Tuple):
                                return_elements = types.elts
                            else:
                                return_elements = [types]
                        else:
                            return_elements = []

                        return_info = []
                        for name, typ in zip(elements, return_elements):
                            if isinstance(name, ast.Name):
                                var_name = name.id
                            else:
                                var_name = ast.unparse(name)

                            var_type = ast.unparse(typ)
                            return_info.append(
                                {"name": var_name, "type_hint": var_type}
                            )
                        return return_info

        return None

    @classmethod
    def extract_arg_info(cls, source: str) -> Dict[str, str]:
        tree = ast.parse(source)
        func_def = tree.body[0]

        arg_info_list = []
        total_args = len(func_def.args.args)
        total_defaults = len(func_def.args.defaults)

        for i, arg in enumerate(func_def.args.args):
            name = arg.arg
            if arg.annotation:
                type_hint = ast.unparse(arg.annotation)
            else:
                type_hint = None

            default_value = None
            if i >= total_args - total_defaults:
                default_index = i - (total_args - total_defaults)
                default_value = func_def.args.defaults[default_index]
                default_value = ast.unparse(default_value)

            arg_info_list.append(
                {"name": name, "type_hint": type_hint, "default": default_value}
            )

        return arg_info_list

    @classmethod
    def extract_return_type(cls, source: str) -> str:
        tree = ast.parse(source)
        func_def = tree.body[0]

        if func_def.returns:
            return_type = ast.unparse(func_def.returns)
        else:
            return_type = None

        return return_type
