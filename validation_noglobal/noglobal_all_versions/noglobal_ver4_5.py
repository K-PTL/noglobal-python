#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, Optional, Callable, Any
from types import FunctionType
import inspect
from functools import partial

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


global noglobal5_2
class noglobal5_2:
    def __init__(self, excepts=None):
        self.excepts = excepts
    
    def __call__(self, _func):
        return no_global_variable_decorator(
            ver=5,
            globals_=_func.__globals__
          )(excepts=self.excepts # arg of _no_global_variable
          )(func=_func)          # arg of _bind_globals 
