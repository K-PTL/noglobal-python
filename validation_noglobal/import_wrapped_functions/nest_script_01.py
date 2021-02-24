from noglobal_ver4_5 import no_global_variable_decorator, noglobal5_2
noglobal4 = no_global_variable_decorator(ver=4, globals_=globals())
noglobal5 = no_global_variable_decorator(ver=5, globals_=globals())

val_global = "This is a global variable"

@noglobal4()
def nest_script01_import_func4():
    print("This is nest_script01_import_func4 at script wrapped by `noglobal4`")
    print(val_global)

@noglobal5()
def nest_script01_import_func5():
    print("This is nest_script01_import_func5 at script wrapped by `noglobal5`")
    print(val_global)

@noglobal5_2()
def nest_script01_import_func5_2():
    print("This is nest_script01_import_func5_2 at script wrapped by `noglobal5_2`")
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


if __name__ == "__main__":
    run_function(nest_script01_import_func4)
    run_function(nest_script01_import_func5)
    run_function(nest_script01_import_func5_2)

# % python nest_script_01.py                                                                                                                 (git)-[main]
# This is nest_script01_import_func4 at script wrapped by `noglobal4`
# got NameError with nest_script01_import_func4; 
#          name 'val_global' is not defined

# This is nest_script01_import_func5 at script wrapped by `noglobal5`
# got NameError with nest_script01_import_func5; 
#          name 'val_global' is not defined

# This is nest_script01_import_func5_2 at script wrapped by `noglobal5_2`
# got NameError with nest_script01_import_func5_2; 
#          name 'val_global' is not defined