# noglobal is one you need

Hey guys!! We have a gift for you!!

## What's `noglobal`

`noglobal` is the decorator that makes your Python code more strictly one with the global variables. No global variables will be worked in the function wrapped by `noglobal` decorator unless set specifically explicit arguments as 'excepts'.

Note that you could not use the global variables that is not able to call, not module, or not specified as 'excepts'.


## How to use

### Install

No PyPI, so you can't use command as `pip`. If you wanna use `noglobal`, please copy the code or clone this repository;

`git clone https://github.com/K-PTL/noglobal-python`

### Example

```python
from noglobal import noglobal

a = "hoge"

def runner(f):
    try:
        f()
    except NameError as ne:
        print(ne)
    print() # blank row


@noglobal()
def func_usual():
    print("This is func_usual")
    print(a) # raised NameError: name 'a' is not defined.


import numpy as np
@noglobal()
def func_nest():
    print("This is func_nest")
    print(np.arange(0,10)) # you can use module as numpy
    print(a)               # raised NameError: name 'a' is not defined.
    run(func_usual())      # you can call it, but raised NameError inside the func_usual.


@noglobal(excepts=["a"])
def func_use_excepts():
    print("This is func_use_excepts")
    print(np.arange(0,10))
    print(a)         # NO NameError raised since specified 'a' as 'excepts'.
    run(func_nest()) # Raised NameError because func_nest does not allow to 
                     # use global variable 'a' while allowed to use in func_use_excepts.


>>> runner(func_usual)
This is func_usual
name 'a' is not defined

>>> runner(func_nest)
This is func_nest
[0 1 2 3 4 5 6 7 8 9]
name 'a' is not defined

>>> runner(func_use_excepts)
This is func_use_excepts
[0 1 2 3 4 5 6 7 8 9]
hoge
This is func_nest
[0 1 2 3 4 5 6 7 8 9]
name 'a' is not defined
```


## Acknowledgement

I introduce you the previous `noglobal` as below;

- [noglobal::ver01 by ax3l](https://gist.github.com/ax3l/59d92c6e1edefcef85ac2540eb056da3)  
- [noglobal::ver02 by raven38](https://gist.github.com/raven38/4e4c3c7a179283c441f575d6e375510c)  
- [noglobal::ver03 by yoshipon](https://gist.github.com/yoshipon/3adba8cc5d7daac6c3256c9163f48920)  
- [noglobal::ver03-2 by K-PTL](https://gist.github.com/K-PTL/8c5cd27a963cec3fc32ad636d433fd77)
- [noglobal::ver04 by momijiame](https://gist.github.com/momijiame/bebf8d4c16fc0916fd80530ebe961525)

My `noglobal` function was builded on what has been laid down by previous contributers. Thanks so much.