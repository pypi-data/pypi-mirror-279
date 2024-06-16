from ._get_func_info import _GetArgInfoHolder


def extract_arg_info(source: str):
    extract_arg_info.__doc__ = _GetArgInfoHolder.extract_arg_info.__doc__
    return _GetArgInfoHolder.extract_arg_info(source)


def extract_return_info(source: str):
    extract_return_info.__doc__ = _GetArgInfoHolder.extract_return_info.__doc__
    return _GetArgInfoHolder.extract_return_info(source)


def extract_return_type(source: str):
    extract_return_type.__doc__ = _GetArgInfoHolder.extract_return_type.__doc__
    return _GetArgInfoHolder.extract_return_type(source)
