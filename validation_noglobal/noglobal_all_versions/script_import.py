# 使用するnoglobal があくまで import されて来た場合

from noglobal_ver1_2_3 import noglobal1, noglobal2, noglobal3, noglobal3_2
from noglobal_ver4_5 import no_global_variable_decorator, noglobal5_2
noglobal4 = no_global_variable_decorator(ver=4, globals_=globals())
noglobal5 = no_global_variable_decorator(ver=5, globals_=globals())

a_global = "This is a global scriptvariable"

def script_import_func():
    print("This is func at script")
    b_local = "This is a local scriptvariable"
    print(b_local)
    print(a_global)

@noglobal1
def script_import_func1():
    print("This is func1 at script wrapped by `noglobal1`")
    b_local = "This is a local scriptvariable"
    print(b_local)
    print(a_global)

@noglobal2
def script_import_func2():
    print("This is func2 at script wrapped by `noglobal2`")
    b_local = "This is a local scriptvariable"
    print(b_local)
    print(a_global)

@noglobal3
def script_import_func3():
    print("This is func3 at script wrapped by `noglobal3`")
    b_local = "This is a local scriptvariable"
    print(b_local)
    print(a_global)

@noglobal3_2
def script_import_func3_2():
    print("This is func3_2 at script wrapped by `noglobal3_2`")
    b_local = "This is a local scriptvariable"
    print(b_local)
    print(a_global)

@noglobal4()
def script_import_func4():
    print("This is func4 at script wrapped by `noglobal4`")
    b_local = "This is a local scriptvariable"
    print(b_local)
    print(a_global)

@noglobal5()
def script_import_func5():
    print("This is func5 at script wrapped by `noglobal5`")
    b_local = "This is a local scriptvariable"
    print(b_local)
    print(a_global)

@noglobal5_2()
def script_import_func5_2():
    print("This is func5-2 at script wrapped by `noglobal5_2`")
    b_local = "This is a local scriptvariable"
    print(b_local)
    print(a_global)


def run_function(func):
    try:
        func()
    except NameError as ne:
        print(f"got NameError with {func.__name__}; ")
        print('\t', ne)
    except TypeError as te:
        print(f"got TypeError with {func.__name__}; ")
        print('\t', te)
    return None

if __name__ == "__main__":
    run_function(script_import_func)
    run_function(script_import_func1)
    run_function(script_import_func2)
    run_function(script_import_func3)
    run_function(script_import_func3_2)
    run_function(script_import_func4)
    run_function(script_import_func5)
    run_function(script_import_func5_2)

# % python script_import.py                                                                                                                  (git)-[main]
# This is func at script
# This is a local scriptvariable
# This is a global scriptvariable
# got NameError with script_import_func1; 
#          name 'print' is not defined
# got NameError with script_import_func2; 
#          name 'print' is not defined
# got TypeError with wrapper; 
#          'NoneType' object is not subscriptable
# got NameError with wrapper; 
#          name 'print' is not defined
# This is func4 at script wrapped by `noglobal4`
# This is a local scriptvariable
# got NameError with script_import_func4; 
#          name 'a_global' is not defined
# This is func5 at script wrapped by `noglobal5`
# This is a local scriptvariable
# got NameError with script_import_func5; 
#          name 'a_global' is not defined
# This is func5-2 at script wrapped by `noglobal5_2`
# This is a local scriptvariable
# got NameError with script_import_func5_2; 
#          name 'a_global' is not defined