import sys

def sequential_map(*args):
    """Takes several functions and a container and returns a list 
    of all container values after sequentional applying of functions to them"""
    funcs = args[:-1]
    container = args[-1]
    for func in funcs:
        container = list(map(func, container))
    return container


def consensus_filter(*args):
    """Takes any number of functions that return True or False and a container with values
    and returns a list of values that passed all functions with True"""
    funcs = args[:-1]
    container = args[-1]
    for func in funcs:
        container = list(filter(func, container))
    return container


def conditional_reduce(func1, func2, container):
    """Takes 2 functions and a container and returns a single value 
    which is the result of reduce after skipping values that did
    not pass the condition of the first function"""
    container = list(filter(func1, container))
    result = container[0]
    for nxt in container[1:]:
        result = func2(result, nxt)
    return result


def func_chain(*args):
    """Takes any number of functions as arguments and returns
    a function concatenating of them by sequential execution"""
    def result_func(val):
        result = val
        for func in args:
            result = func(result)
        return result
    return result_func


def sequential_map_2(*args):
    """Realization of sequentional_map using func_chain"""
    funcs = args[:-1]
    vals = args[-1]
    func = func_chain(*funcs)
    return list(func(vals))


def single_partial(func, **kwargs):
    """Takes one function and any named arguments and returns 
    this function with arguments pre-set"""
    def inner_func(*args_by_user):
        return func(*args_by_user, **kwargs)
    return inner_func


def multiple_partial(*funcs, **kwargs):
    """Takes any number of functions and named arguments 
    and returns the list of functions with arguments pre-set"""
    result = [single_partial(func, **kwargs) for func in funcs]
    return result


def print_analogue(*args, end="\n", sep=" ", file=sys.stdout):
    """Print function analogue"""
    parts_to_type = [str(x) for x in args]
    all_parts = sep.join(parts_to_type)
    file.write(f'{all_parts}{end}')