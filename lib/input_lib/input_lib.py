import os
import ctypes

# TODO: Docs

if __name__ == "__main__":
    lib = ctypes.CDLL(os.getcwd()+"/lib.so")
else:
    lib = ctypes.CDLL(os.getcwd()+"/lib/search_input/lib.so")

lib.input_search.restype = ctypes.c_char_p
lib.counter.restype = ctypes.c_int
lib.checker.restype = ctypes.c_bool

def search_input(prompt: str, tips: list[str]):
    c_prompt = ctypes.c_char_p(prompt.encode('ascii'))

    c_tips = (ctypes.c_char_p * len(tips))()
    c_tips[:] = [s.encode('ascii') for s in tips]
    n = len(tips)

    c_string = lib.input_search(c_prompt, c_tips, n)

    return ctypes.string_at(c_string).decode('ascii')

def counter(prompt: str, default: int, min: int, max: int):
    c_prompt = ctypes.c_char_p(prompt.encode('ascii'))

    return lib.counter(c_prompt, default, min, max)
    
def checker(prompt: str, def_val: bool):
    c_prompt = ctypes.c_char_p(prompt.encode('ascii'))

    return lib.checker(c_prompt, def_val)


