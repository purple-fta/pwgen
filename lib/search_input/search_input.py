import os
import ctypes

# TODO: Docs

lib = ctypes.CDLL(os.getcwd()+"/lib/search_input/lib.so")


def search_input(prompt: str, tips: list[str]):
    c_prompt = ctypes.c_char_p(prompt.encode('ascii'))

    c_tips = (ctypes.c_char_p * len(tips))()
    c_tips[:] = [s.encode('ascii') for s in tips]
    n = len(tips)
    return_text = " " * 100
    c_string = ctypes.c_char_p(return_text.encode('ascii'))
    c_string_ptr = ctypes.pointer(c_string)

    lib.input_search(c_prompt, c_tips, n, c_string_ptr)

    return ctypes.string_at(c_string_ptr).decode('utf-8')

