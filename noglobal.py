from functools import partial
import inspect
from typing import List, Dict, Optional, Callable, Any
from types import FunctionType

# Function prototype
# this is not necessary, just my pray for.
global noglobal


# https://gist.github.com/momijiame/bebf8d4c16fc0916fd80530ebe961525
def globals_with_module_and_callable(globals_: Optional[Dict[str, Any]] = None,
                                     excepts: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    :param globals_: base global symbol table
    :param excepts: List[str], involve the names of variables which is expected to be included into global symbol table
    :return: Dict[str, Any], global symbol table
    """
    def need(name, attr) -> bool:
        """ if attr is need or name is in excepts, then return True, otherwise return False. """
        if name in excepts:
            return True
        if inspect.ismodule(attr):
            return True
        if callable(attr):
            return True
        return False
    
    if globals_ is None:
        globals_ = globals()
    if excepts is None:
        excepts = []
    
    filtered_globals = {
        name: attr
        for name, attr in globals_.items()
        if need(name, attr)
    }
    
    # If __name__ == "__main__", then we do not have to consider the dealing of builtins (globals()["__builtins__"] is <module 'builtins' (built-in)>).
    # However, if __name__ != "__main__", then globals()["__builtins__"] has the builtins in similar with global variables (not module).
    if not inspect.ismodule(globals_["__builtins__"]):
        for name, attr in globals_["__builtins__"].items():
            if need(name, attr): filtered_globals[name] = attr
    
    return filtered_globals


def bind_globals(globals_: Dict[str, Any]) -> Callable:
    """ decorator returning functional object for wrapping, which run the callable object on the specified global symbol table.
    :param globals_: global symbol table
    :returns: functional object for wrapping
    """
    def _bind_globals(func: FunctionType) -> FunctionType:
        bound_func = FunctionType(code=func.__code__,
                                  globals=globals_,
                                  name=func.__name__,
                                  argdefs=func.__defaults__,
                                  closure=func.__closure__,
                                  )
        return bound_func
    return _bind_globals


def no_global_variable_decorator(globals_: Optional[Dict[str, Any]] = None):
    """ Providing the decorator of inhibiting the use of global variables """
    partialled = partial(globals_with_module_and_callable, globals_=globals_)

    def _no_global_variable(excepts: Optional[List[str]] = None):
        partialled_globals_ = partialled(excepts=excepts)
        bound_func = bind_globals(globals_=partialled_globals_)
        return bound_func
    return _no_global_variable


# substance of noglobal function
class noglobal:
    def __init__(self, excepts=None):
        self.excepts = excepts
    
    def __call__(self, _func):
        return no_global_variable_decorator(
            globals_=_func.__globals__
          )(excepts=self.excepts # arg of _no_global_variable
          )(func=_func)          # arg of _bind_globals 


if __name__ == "__main__":
    # from noglobal import noglobal
    a = "hoge"
    
    def run(f):
        try:
            f()
        except NameError as ne:
            print(ne)
        print()

    @noglobal()
    def func_usual():
        print("This is func_usual")
        print(a)

    import numpy as np
    @noglobal()
    def func_nest():
        print("This is func_nest")
        print(np.arange(0,10))
        print(a)
        run(func_usual())

    @noglobal(excepts=["a"])
    def func_use_excepts():
        print("This is func_use_excepts")
        print(np.arange(0,10))
        print(a)
        run(func_nest()) # Raised NameError because func_nest
                         # does not allow to use global variable; a.
    
    run(func_usual)
    run(func_nest)
    run(func_use_excepts)
# end if