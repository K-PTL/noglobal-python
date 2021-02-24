import builtins
import inspect
from types import FunctionType, ModuleType

def imports():
    for name, val in globals().items():
        # module imports
        if isinstance(val, ModuleType):
            yield name, val

            # functions / callables
        if hasattr(val, '__call__'):
            yield name, val


# https://gist.github.com/ax3l/59d92c6e1edefcef85ac2540eb056da3
noglobal1 = lambda fn: FunctionType(fn.__code__, dict(imports()))


def noglobal2(f):
    '''
    https://gist.github.com/yoshipon/3adba8cc5d7daac6c3256c9163f48920
    '''
    return FunctionType(f.__code__,
                        dict(imports()),
                        f.__name__,
                        f.__defaults__,
                        f.__closure__
                        )


def noglobal3(fn):
    # https://gist.github.com/yoshipon/3adba8cc5d7daac6c3256c9163f48920
    fn_noglobal = FunctionType(fn.__code__, dict(imports()))
    arg_info = inspect.getfullargspec(fn)
    
    def wrapper(*wrapper_args, **wrapper_kwargs):

        kwargs = dict((k, v) for k, v in zip(arg_info.args[::-1], arg_info.defaults[::-1]))
        for k, v in zip(arg_info.args, wrapper_args):
            kwargs[k] = v
        for k, v in wrapper_kwargs.items():
            kwargs[k] = v

        return fn_noglobal(**kwargs)
        
    return wrapper


def noglobal3_2(fn):
    # https://gist.github.com/yoshipon/3adba8cc5d7daac6c3256c9163f48920
    fn_noglobal = FunctionType(fn.__code__, dict(imports()))
    arg_info = inspect.getfullargspec(fn)
    
    def wrapper(*wrapper_args, **wrapper_kwargs):
        if not arg_info.defaults is None:
            kwargs = dict((k, v) for k, v in zip(arg_info.args[::-1], arg_info.defaults[::-1]))
        else:
            kwargs = dict()
            
        for k, v in zip(arg_info.args, wrapper_args):
            kwargs[k] = v
        for k, v in wrapper_kwargs.items():
            kwargs[k] = v

        return fn_noglobal(**kwargs)
        
    return wrapper
