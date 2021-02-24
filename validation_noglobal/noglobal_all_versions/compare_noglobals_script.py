# Import noglobal decorators

from noglobal_ver1_2_3 import noglobal1, noglobal2, noglobal3, noglobal3_2
from noglobal_ver4_5 import no_global_variable_decorator, noglobal5_2
noglobal4 = no_global_variable_decorator(ver=4, globals_=globals())
noglobal5 = no_global_variable_decorator(ver=5, globals_=globals())


val_global = "This is a global variable"

def script_import_func():
    print("This is func at script with import noglobal (without)")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal1
def script_import_func1():
    print("This is func1 at script wrapped by import `noglobal1`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal2
def script_import_func2():
    print("This is func2 at script wrapped by import `noglobal2`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal3
def script_import_func3():
    print("This is func3 at script wrapped by import `noglobal3`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal3_2
def script_import_func3_2():
    print("This is func3_2 at script wrapped by import `noglobal3_2`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal4()
def script_import_func4():
    print("This is func4 at script wrapped by import `noglobal4`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal5()
def script_import_func5():
    print("This is func5 at script wrapped by import `noglobal5`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal5_2()
def script_import_func5_2():
    print("This is func5_2 at script wrapped by import `noglobal5_2`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

def run_function(func):
    try:
        func()
    except NameError as ne:
        print(f"got NameError with {func.__name__}; ")
        print('\t', ne)
    except TypeError as te: # noglobal::ver03 でのみ発生
        print(f"got TypeError with {func.__name__}; ")
        print('\t', te)
    print() # blank row
    return None

print("## run function with import noglobals")
run_function(script_import_func)
run_function(script_import_func1)
run_function(script_import_func2)
run_function(script_import_func3)
run_function(script_import_func3_2)
run_function(script_import_func4)
run_function(script_import_func5)
run_function(script_import_func5_2)

# +++++++++

# write down all noglobal decorators inline

import builtins
from functools import partial
import inspect
from typing import List, Dict, Optional, Callable, Any
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


# https://gist.github.com/momijiame/bebf8d4c16fc0916fd80530ebe961525
def globals_with_module_and_callable_ver4(globals_: Optional[Dict[str, Any]] = None,
                                     excepts: Optional[List[str]] = None) -> Dict[str, Any]:
    """モジュールと呼び出し可能オブジェクトだけが含まれるグローバルシンボルテーブルを返す関数
    :param globals_: 別のモジュールからインポートして使う場合、globals() の結果を入れる
    :param excepts: 例外的に含めたいグローバル変数の名前を含むリストオブジェクト
    :return: モジュールと呼び出し可能オブジェクトだけを含む辞書オブジェクト
    """
    def need(name, attr):
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
    return filtered_globals


def globals_with_module_and_callable_ver5(globals_: Optional[Dict[str, Any]] = None,
                                     excepts: Optional[List[str]] = None) -> Dict[str, Any]:
    """モジュールと呼び出し可能オブジェクトだけが含まれるグローバルシンボルテーブルを返す関数
    :param globals_: 別のモジュールからインポートして使う場合、globals() の結果を入れる
    :param excepts: 例外的に含めたいグローバル変数の名前を含むリストオブジェクト
    :return: モジュールと呼び出し可能オブジェクトだけを含む辞書オブジェクト
    """
    def need(name, attr):
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
    
    # __name__ == "__main__" でないとき、globals()["__builtins__"] の中に global変数と同じ形式でbuiltinsが並んでいる
    # __name__ == "__main__" の時は builtins 自体がモジュール(<module 'builtins' (built-in)>)なので追加されるが、そうでないときは明示して追加する必要がある
    if not inspect.ismodule(globals_["__builtins__"]):
        for name, attr in globals_["__builtins__"].items():
            if need(name, attr): filtered_globals[name] = attr
    
    return filtered_globals


def bind_globals(globals_: Dict[str, Any]) -> Callable:
    """呼び出し可能オブジェクトを特定のグローバルシンボルテーブルで実行するようにラップする関数を返すデコレータ
    :param globals_: 制約したいグローバルシンボルテーブル
    :returns: ラップするのに使う関数オブジェクト
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


def no_global_variable_decorator(ver=4, globals_: Optional[Dict[str, Any]] = None):
    """グローバル変数を使えなくするデコレータを返す高階関数"""
    if ver == 4: 
        partialled = partial(globals_with_module_and_callable_ver4, globals_=globals_)
    if ver == 5: 
        partialled = partial(globals_with_module_and_callable_ver5, globals_=globals_)

    def _no_global_variable(excepts: Optional[List[str]] = None):
        partialled_globals_ = partialled(excepts=excepts)
        bound_func = bind_globals(globals_=partialled_globals_)
        return bound_func

    return _no_global_variable

noglobal4 = no_global_variable_decorator(ver=4, globals_=globals())
noglobal5 = no_global_variable_decorator(ver=5, globals_=globals())

class noglobal5_2:
    def __init__(self, excepts=None):
        self.excepts = excepts
    
    def __call__(self, _func):
        return no_global_variable_decorator(
            globals_=_func.__globals__
          )(excepts=self.excepts # arg of _no_global_variable
          )(func=_func)          # arg of _bind_globals 


val_global = "This is a global variable"

def script_inline_func():
    print("This is func at script with inline noglobal (without)")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal1
def script_inline_func1():
    print("This is func1 at script wrapped by inline `noglobal1`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal2
def script_inline_func2():
    print("This is func2 at script wrapped by inline `noglobal2`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal3
def script_inline_func3():
    print("This is func3 at script wrapped by inline `noglobal3`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal3_2
def script_inline_func3_2():
    print("This is func3_2 at script wrapped by inline `noglobal3_2`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal4()
def script_inline_func4():
    print("This is func4 at script wrapped by inline `noglobal4`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal5()
def script_inline_func5():
    print("This is func5 at script wrapped by inline `noglobal5`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

@noglobal5_2()
def script_inline_func5_2():
    print("This is func5_2 at script wrapped by inline `noglobal5_2`")
    val_local = "This is a local variable"
    print(val_local)
    print(val_global)

def run_function(func):
    try:
        func()
    except NameError as ne:
        print(f"got NameError with {func.__name__}; ")
        print('\t', ne)
    except TypeError as te: # noglobal::ver03 でのみ発生
        print(f"got TypeError with {func.__name__}; ")
        print('\t', te)
    print() # blank row
    return None

print("## run function with inline noglobals")
run_function(script_inline_func)
run_function(script_inline_func1)
run_function(script_inline_func2)
run_function(script_inline_func3)
run_function(script_inline_func3_2)
run_function(script_inline_func4)
run_function(script_inline_func5)
run_function(script_inline_func5_2)