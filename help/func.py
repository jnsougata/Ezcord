from functools import wraps

l = []
m = []

def pre_dec(rn:str):
    m.append(rn)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            l.append(func.__name__)
        return wrapper
    return decorator



@pre_dec('XYZ')
def hello_func(param):
    print(param)


hello_func('hello')
print(l)
print(m)