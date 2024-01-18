import os
import ctypes


if __name__ == "__main__":
    lib = ctypes.CDLL(os.getcwd()+"/lib.so")
else:
    lib = ctypes.CDLL(os.getcwd()+"/lib/search_input/lib.so")


lib.input_search.restype = ctypes.c_char_p
lib.counter.restype = ctypes.c_int
lib.checker.restype = ctypes.c_bool


def search_input(promt: str, tips: list[str]) -> str:
    """Inpu with prompt and search by string in c_tips

    Args:
        prompt: String with promt 
        tips: List of strings to search for

    Returns:
        A string with the text entered by the user or text from the search
    """
    
    # Conver python string to C string
    c_promt = ctypes.c_char_p(promt.encode('ascii'))


    c_tips = (ctypes.c_char_p * len(tips))()
    c_tips[:] = [s.encode('ascii') for s in tips]
    
    n = len(tips)

    c_string = lib.input_search(c_promt, c_tips, n)

    # Conver to Python string and return
    return ctypes.string_at(c_string).decode('ascii')

def counter(promt: str, default: int, min: int, max: int) -> int:
    # Conver python string to C string
    c_promt = ctypes.c_char_p(promt.encode('ascii'))

    return lib.counter(c_promt, default, min, max)
    
def checker(promt: str, def_val: bool) -> bool:
    # Conver python string to C string
    c_promt = ctypes.c_char_p(promt.encode('ascii'))

    return lib.checker(c_promt, def_val)


